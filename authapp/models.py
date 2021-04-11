from django.db import models
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12,blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic', blank=True)
    email_pref = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
