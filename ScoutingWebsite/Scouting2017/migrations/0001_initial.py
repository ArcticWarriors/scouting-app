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
                ('competition', models.ForeignKey(to='Scouting2017.Compitition')),
            ],
        ),
        migrations.CreateModel(
            name='OfficialMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matchNumber', models.IntegerField()),
                ('hasOfficialData', models.BooleanField(default=False)),
                ('competition', models.ForeignKey(to='Scouting2017.Compitition')),
            ],
        ),
        migrations.CreateModel(
            name='OfficialMatchScoreResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('competition', models.ForeignKey(to='Scouting2017.Compitition')),
                ('official_match', models.ForeignKey(to='Scouting2017.OfficialMatch')),
            ],
        ),
        migrations.CreateModel(
            name='ScoreResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('competition', models.ForeignKey(to='Scouting2017.Compitition')),
                ('match', models.ForeignKey(to='Scouting2017.Match')),
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
                ('competition', models.ForeignKey(to='Scouting2017.Compitition')),
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
                ('team', models.OneToOneField(to='Scouting2017.Team')),
            ],
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='team',
            field=models.ForeignKey(to='Scouting2017.Team'),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='team1',
            field=models.ForeignKey(related_name='da_team1', to='Scouting2017.Team'),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='team2',
            field=models.ForeignKey(related_name='da_team2', to='Scouting2017.Team'),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='team3',
            field=models.ForeignKey(related_name='da_team3', to='Scouting2017.Team'),
        ),
    ]
