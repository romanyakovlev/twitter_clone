from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
# Create your models here.

class Tweet(models.Model):
    text = models.CharField(max_length = 140)
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now = True)

class Follow(models.Model):
    person = models.OneToOneField(User,null = True)
    follows = models.ManyToManyField(User,related_name='follows')

class Like(models.Model):
    person = models.ManyToManyField(User,related_name='person')
    tweet = models.ForeignKey(Tweet,null=True,related_name='likes')

class Comments(models.Model):
    comment = models.ForeignKey(Tweet,null=True)
    user = models.ForeignKey(User)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(default='default_avatar.jpeg') # Только в DEBUG MODE
