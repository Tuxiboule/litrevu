from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Model for User
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    follower = models.ManyToManyField('self', symmetrical=False, related_name='followings')
