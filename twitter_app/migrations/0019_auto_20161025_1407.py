# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-25 14:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_app', '0018_auto_20161021_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='twitter_app.Tweet'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='default_avatar.jpeg', upload_to=''),
        ),
    ]
