# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 17:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('twitter_app', '0011_auto_20161002_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='person',
        ),
        migrations.AddField(
            model_name='like',
            name='person',
            field=models.ManyToManyField(related_name='person', to=settings.AUTH_USER_MODEL),
        ),
    ]
