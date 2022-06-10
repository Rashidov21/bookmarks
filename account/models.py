from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    followers = models.PositiveIntegerField(default=0)
    follows = models.PositiveIntegerField(default=0)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(default='media/cool.png', upload_to='users/%Y/%m/%d/',
                              blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class Followers(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    another_user = models.ManyToManyField(
        User, related_name='another_user')

    def __str__(self):
        return self.user.username
