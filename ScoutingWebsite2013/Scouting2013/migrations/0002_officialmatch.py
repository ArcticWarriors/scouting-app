# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2013', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficialMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matchNumber', models.IntegerField()),
                ('redTeam1', models.IntegerField()),
                ('redTeam2', models.IntegerField()),
                ('redTeam3', models.IntegerField()),
                ('blueTeam1', models.IntegerField()),
                ('blueTeam2', models.IntegerField()),
                ('blueTeam3', models.IntegerField()),
                ('redScore', models.IntegerField(default=-1)),
                ('blueScore', models.IntegerField(default=-1)),
            ],
        ),
    ]
