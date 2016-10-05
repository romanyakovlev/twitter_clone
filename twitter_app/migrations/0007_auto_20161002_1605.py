# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 16:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_app', '0006_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='likes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='twitter_app.Tweet'),
        ),
        migrations.AlterField(
            model_name='like',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]