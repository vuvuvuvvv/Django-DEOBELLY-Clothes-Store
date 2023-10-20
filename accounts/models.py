from django.db import models
from system.constant import IMG_UNKNOWN_USER
from django.contrib.auth.models import AbstractUser

#Settings.py:  AUTH_USER_MODEL = 'your_app.CustomUser'
class User(AbstractUser):
    tel = models.CharField(max_length=15, blank= True)
    avatar = models.URLField(blank=True, default=IMG_UNKNOWN_USER)
    is_verified = models.IntegerField(default=0) #0: not verified, 1: verified
