# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0021_auto_20160328_1758'),
    ]

    operations = [
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
                ('official_match', models.ForeignKey(to='Scouting2016.OfficialMatch')),
                ('team1', models.ForeignKey(related_name='da_team1', to='Scouting2016.Team')),
                ('team2', models.ForeignKey(related_name='da_team2', to='Scouting2016.Team')),
                ('team3', models.ForeignKey(related_name='da_team3', to='Scouting2016.Team')),
            ],
        ),
    ]
