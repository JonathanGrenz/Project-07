# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-12-09 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='confirm_email',
            field=models.EmailField(default='', max_length=254),
            preserve_default=False,
        ),
    ]