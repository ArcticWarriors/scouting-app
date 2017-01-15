# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Compitition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matchNumber', models.IntegerField()),
                ('competition', models.ForeignKey(to='Scouting2015.Compitition')),
            ],
        ),
        migrations.CreateModel(
            name='OfficialMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matchNumber', models.IntegerField()),
                ('hasOfficialData', models.BooleanField(default=False)),
                ('competition', models.ForeignKey(to='Scouting2015.Compitition')),
            ],
        ),
        migrations.CreateModel(
            name='OfficialMatchScoreResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('autonA', models.CharField(default=b'None', max_length=20)),
                ('autonB', models.CharField(default=b'None', max_length=20)),
                ('autonC', models.CharField(default=b'None', max_length=20)),
                ('autoBouldersLow', models.IntegerField(default=-1)),
                ('autoBouldersHigh', models.IntegerField(default=-1)),
                ('teleBouldersLow', models.IntegerField(default=-1)),
                ('teleBouldersHigh', models.IntegerField(default=-1)),
                ('teleDefenseCrossings', models.IntegerField(default=-1)),
                ('defense1Crossings', models.IntegerField(default=-1)),
                ('defense2Name', models.CharField(default=b'Unspecified', max_length=20)),
                ('defense2Crossings', models.IntegerField(default=-1)),
                ('defense3Name', models.CharField(default=b'Unspecified', max_length=20)),
                ('defense3Crossings', models.IntegerField(default=-1)),
                ('defense4Name', models.CharField(default=b'Unspecified', max_length=20)),
                ('defense4Crossings', models.IntegerField(default=-1)),
                ('defense5Name', models.CharField(default=b'Unspecified', max_length=20)),
                ('defense5Crossings', models.IntegerField(default=-1)),
                ('towerFaceA', models.CharField(default=b'none', max_length=20)),
                ('towerFaceB', models.CharField(default=b'none', max_length=20)),
                ('towerFaceC', models.CharField(default=b'none', max_length=20)),
                ('fouls', models.IntegerField(default=-1)),
                ('techFouls', models.IntegerField(default=-1)),
                ('competition', models.ForeignKey(to='Scouting2015.Compitition')),
                ('official_match', models.ForeignKey(to='Scouting2015.OfficialMatch')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teamNumber', models.IntegerField()),
                ('homepage', models.CharField(default=b'', max_length=2000)),
                ('rookie_year', models.CharField(max_length=4)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('team_name', models.CharField(max_length=100)),
                ('team_nickname', models.CharField(max_length=100)),
                ('robot_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TeamComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=1000)),
                ('team', models.ForeignKey(to='Scouting2015.Team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamCompetesIn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('competition', models.ForeignKey(to='Scouting2015.Compitition')),
                ('team', models.ForeignKey(to='Scouting2015.Team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamPictures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=1000)),
                ('team', models.ForeignKey(to='Scouting2015.Team')),
            ],
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='team1',
            field=models.ForeignKey(related_name='da_team1', to='Scouting2015.Team'),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='team2',
            field=models.ForeignKey(related_name='da_team2', to='Scouting2015.Team'),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='team3',
            field=models.ForeignKey(related_name='da_team3', to='Scouting2015.Team'),
        ),
    ]
