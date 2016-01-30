# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-30 18:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0005_auto_20160128_1816'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamPictures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=1000)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Scouting2016.Team')),
            ],
        ),
    ]
