from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField('昵称', max_length=50, blank=True)
    avatar = models.ImageField('头像', upload_to='static/avatar/%Y/%M', default="static/avatar/default.png", max_length=100)

    def __str__(self):
        return self.nickname
