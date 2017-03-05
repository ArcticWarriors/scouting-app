# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('week', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matchNumber', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OfficialMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matchNumber', models.IntegerField()),
                ('hasOfficialData', models.BooleanField(default=False)),
                ('competition', models.ForeignKey(to='Scouting2017.Competition')),
            ],
        ),
        migrations.CreateModel(
            name='OfficialMatchScoreResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alliance_color', models.CharField(max_length=1, choices=[(b'R', b'Red'), (b'B', b'Blue')])),
                ('robot1Auto', models.CharField(default=b'', max_length=2000)),
                ('robot2Auto', models.CharField(default=b'', max_length=2000)),
                ('robot3Auto', models.CharField(default=b'', max_length=2000)),
                ('autoFuelLow', models.IntegerField(default=0)),
                ('autoFuelHigh', models.IntegerField(default=0)),
                ('rotor1Auto', models.IntegerField(default=0)),
                ('rotor2Auto', models.IntegerField(default=0)),
                ('teleopFuelLow', models.IntegerField(default=0)),
                ('teleopFuelHigh', models.IntegerField(default=0)),
                ('rotor1Engaged', models.IntegerField(default=0)),
                ('rotor2Engaged', models.IntegerField(default=0)),
                ('rotor3Engaged', models.IntegerField(default=0)),
                ('rotor4Engaged', models.IntegerField(default=0)),
                ('touchpadNear', models.IntegerField(default=0)),
                ('touchpadMiddle', models.IntegerField(default=0)),
                ('touchpadFar', models.IntegerField(default=0)),
                ('foulCount', models.IntegerField(default=0)),
                ('techFoulCount', models.IntegerField(default=0)),
                ('autoMobilityPoints', models.IntegerField(default=0)),
                ('autoRotorPoints', models.IntegerField(default=0)),
                ('autoPoints', models.IntegerField(default=0)),
                ('teleopFuelPoints', models.IntegerField(default=0)),
                ('teleopRotorPoints', models.IntegerField(default=0)),
                ('teleopTakeoffPoints', models.IntegerField(default=0)),
                ('teleopPoints', models.IntegerField(default=0)),
                ('foulPoints', models.IntegerField(default=0)),
                ('totalPoints', models.IntegerField(default=0)),
                ('kPaRankingPointAchieved', models.BooleanField(default=False)),
                ('rotorRankingPointAchieved', models.BooleanField(default=False)),
                ('competition', models.ForeignKey(to='Scouting2017.Competition')),
                ('official_match', models.ForeignKey(to='Scouting2017.OfficialMatch')),
            ],
        ),
        migrations.CreateModel(
            name='PickList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grouping', models.CharField(max_length=1000)),
                ('rank_in_group', models.IntegerField(default=1)),
                ('competition', models.ForeignKey(to='Scouting2017.Competition')),
            ],
        ),
        migrations.CreateModel(
            name='ScoreResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auto_gears', models.IntegerField(default=0)),
                ('auto_fuel_high_shots', models.IntegerField(default=0)),
                ('auto_fuel_high_score', models.IntegerField(default=0)),
                ('auto_fuel_low_shots', models.IntegerField(default=0)),
                ('auto_fuel_low_score', models.IntegerField(default=0)),
                ('auto_baseline', models.BooleanField(default=False)),
                ('tele_gears', models.IntegerField(default=0)),
                ('tele_fuel_high_shots', models.IntegerField(default=0)),
                ('tele_fuel_high_score', models.IntegerField(default=0)),
                ('tele_fuel_low_shots', models.IntegerField(default=0)),
                ('tele_fuel_low_score', models.IntegerField(default=0)),
                ('rope', models.BooleanField(default=False)),
                ('tech_foul', models.IntegerField(default=0)),
                ('foul', models.IntegerField(default=0)),
                ('red_card', models.BooleanField(default=False)),
                ('yellow_card', models.BooleanField(default=False)),
                ('hoppers_dumped', models.IntegerField(default=0)),
                ('gathered_fuel_from_ground', models.BooleanField(default=False)),
                ('gathered_gear_from_ground', models.BooleanField(default=False)),
                ('match_comments', models.CharField(default=b'', max_length=1000)),
                ('competition', models.ForeignKey(to='Scouting2017.Competition')),
                ('match', models.ForeignKey(to='Scouting2017.Match')),
            ],
        ),
        migrations.CreateModel(
            name='Scout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('team', models.ForeignKey(to='Scouting2017.Team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamCompetesIn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('competition', models.ForeignKey(to='Scouting2017.Competition')),
                ('team', models.ForeignKey(to='Scouting2017.Team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamPictures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=1000)),
                ('team', models.ForeignKey(to='Scouting2017.Team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamPitScouting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('competent', models.BooleanField(default=False)),
                ('short_fat', models.BooleanField(default=False)),
                ('tall_wide', models.BooleanField(default=False)),
                ('OrganizedFunctional', models.CharField(default=b'no', max_length=1000)),
                ('FuelCapacity', models.CharField(default=b'no', max_length=1000)),
                ('Gears', models.CharField(default=b'no', max_length=1000)),
                ('Strategy', models.CharField(max_length=1000)),
                ('Size', models.CharField(max_length=1000)),
                ('FuelAcquire', models.CharField(max_length=1000)),
                ('AllianceStrategy', models.CharField(default=b'no', max_length=1000)),
                ('AllanceCompetent', models.CharField(default=b'no', max_length=1000)),
                ('CompetnetConfident', models.CharField(default=b'no', max_length=1000)),
                ('Competitions', models.CharField(default=b'no', max_length=1000)),
                ('Random', models.CharField(max_length=1000)),
                ('team', models.OneToOneField(to='Scouting2017.Team')),
            ],
        ),
        migrations.AddField(
            model_name='scout',
            name='bookmarked_teams',
            field=models.ManyToManyField(related_name='bookmarks', to='Scouting2017.Team'),
        ),
        migrations.AddField(
            model_name='scout',
            name='do_not_pick_teams',
            field=models.ManyToManyField(related_name='do_not_picks', to='Scouting2017.Team'),
        ),
        migrations.AddField(
            model_name='scout',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='team',
            field=models.ForeignKey(to='Scouting2017.Team'),
        ),
        migrations.AddField(
            model_name='picklist',
            name='team',
            field=models.ForeignKey(to='Scouting2017.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='blue1',
            field=models.ForeignKey(related_name='blue1', to='Scouting2017.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='blue2',
            field=models.ForeignKey(related_name='blue2', to='Scouting2017.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='blue3',
            field=models.ForeignKey(related_name='blue3', to='Scouting2017.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='competition',
            field=models.ForeignKey(to='Scouting2017.Competition'),
        ),
        migrations.AddField(
            model_name='match',
            name='red1',
            field=models.ForeignKey(related_name='red1', to='Scouting2017.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='red2',
            field=models.ForeignKey(related_name='red2', to='Scouting2017.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='red3',
            field=models.ForeignKey(related_name='red3', to='Scouting2017.Team'),
        ),
    ]
