# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-19 23:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0007_remove_team_teamally174'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='teamAlly174',
            field=models.CharField(default=2, max_length=3),
            preserve_default=False,
        ),
    ]