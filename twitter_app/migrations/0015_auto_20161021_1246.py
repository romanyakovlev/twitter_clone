# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-21 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_app', '0014_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='default_avatar.jpeg', upload_to='avatars/'),
        ),
    ]
