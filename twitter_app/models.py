from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

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

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(default='default_avatar.jpeg') # Только в DEBUG MODE

class Comments(models.Model):
    text = models.TextField(null=True)
    comment = models.ForeignKey(Tweet,default=0)
    user = models.ForeignKey(UserProfile)
