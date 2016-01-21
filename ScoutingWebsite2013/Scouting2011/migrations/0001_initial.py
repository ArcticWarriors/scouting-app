# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matchNumber', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ScoreResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('TubesDropped', models.IntegerField()),
                ('LowTubesHung', models.IntegerField()),
                ('MidTubesHung', models.IntegerField()),
                ('HighTubesHung', models.IntegerField()),
                ('TubesRecieved', models.IntegerField()),
                ('Penelties', models.IntegerField()),
                ('MiniBotFinish', models.IntegerField()),
                ('DeployedMinibot', models.BooleanField()),
                ('ScoredUberTube', models.BooleanField()),
                ('WasOffensive', models.BooleanField()),
                ('WasScouted', models.BooleanField()),
                ('BrokeBadly', models.BooleanField()),
                ('Comments', models.CharField(max_length=1000)),
                ('match', models.ForeignKey(to='Scouting2011.Match')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teamNumber', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='team',
            field=models.ForeignKey(to='Scouting2011.Team'),
        ),
    ]
