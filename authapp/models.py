from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import user_profile_pic_directory_path

class User(AbstractUser):

    phone_number = models.CharField(
        max_length = 12,
        blank = True
    )
    profile_pic = models.ImageField(
        upload_to = user_profile_pic_directory_path, 
        blank = True
    )
    email_preference = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
