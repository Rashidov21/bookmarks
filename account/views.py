from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Followers
# Create your views here.


@login_required
def dashboard(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard', "users": users})


def follow_user(request, user_name):
    # following user
    user = User.objects.get(username=request.user.username)
    # print(user)
    # will be followed user
    f_user = User.objects.get(username=user_name)
    # print(f_user)
    # following user followers
    user_follower = Followers.objects.get(user=user)

    # check followers
    if f_user not in user_follower.another_user.all():
        user_follower.another_user.add(f_user)
        user_follower.save()

        print(user_follower.another_user)

        f_user.profile.followers += 1
        user.profile.follows += 1
        user.profile.save()
        f_user.profile.save()
        messages.add_message(request, messages.SUCCESS,
                             "You successfuly following this user!")
        return redirect("account:profile", user_name=user_name)
    else:
        messages.add_message(request, messages.WARNING,
                             "You followed this user!")
        return redirect("account:profile", user_name=user_name)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            Profile.objects.create(user=new_user)
            Followers.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request,
                      'account/register.html',
                      {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})


@ login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect("/account/profile/")
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(
                instance=request.user.profile)
        return render(request,
                      'account/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})


@ login_required
def profile(request, user_name):
    user = User.objects.get(username=user_name)

    is_followed = False
    # if user.followers.another_user

    return render(request, "account/profile.html", {"user": user})
