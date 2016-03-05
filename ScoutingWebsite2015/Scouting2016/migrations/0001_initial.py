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
            name='OfficialMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matchNumber', models.IntegerField()),
                ('hasOfficialData', models.BooleanField(default=False)),
                ('redAutoBouldersLow', models.IntegerField(default=-1)),
                ('redAutoBouldersHigh', models.IntegerField(default=-1)),
                ('redTeleBouldersLow', models.IntegerField(default=-1)),
                ('redTeleBouldersHigh', models.IntegerField(default=-1)),
                ('redDefense1Crossings', models.IntegerField(default=-1)),
                ('redDefense2Name', models.CharField(default=b'Unspecified', max_length=20)),
                ('redDefense2Crossings', models.IntegerField(default=-1)),
                ('redDefense3Name', models.CharField(default=b'Unspecified', max_length=20)),
                ('redDefense3Crossings', models.IntegerField(default=-1)),
                ('redDefense4Name', models.CharField(default=b'Unspecified', max_length=20)),
                ('redDefense4Crossings', models.IntegerField(default=-1)),
                ('redDefense5Name', models.CharField(default=b'Unspecified', max_length=20)),
                ('redDefense5Crossings', models.IntegerField(default=-1)),
                ('redTowerFaceA', models.CharField(default=b'none', max_length=20)),
                ('redTowerFaceB', models.CharField(default=b'none', max_length=20)),
                ('redTowerFaceC', models.CharField(default=b'none', max_length=20)),
                ('redFouls', models.IntegerField(default=-1)),
                ('redTechFouls', models.IntegerField(default=-1)),
                ('blueAutoBouldersLow', models.IntegerField(default=-1)),
                ('blueAutoBouldersHigh', models.IntegerField(default=-1)),
                ('blueTeleBouldersLow', models.IntegerField(default=-1)),
                ('blueTeleBouldersHigh', models.IntegerField(default=-1)),
                ('blueDefense1Crossings', models.IntegerField(default=-1)),
                ('blueDefense2Name', models.CharField(default=b'Unspecified', max_length=20)),
                ('blueDefense2Crossings', models.IntegerField(default=-1)),
                ('blueDefense3Name', models.CharField(default=b'Unspecified', max_length=20)),
                ('blueDefense3Crossings', models.IntegerField(default=-1)),
                ('blueDefense4Name', models.CharField(default=b'Unspecified', max_length=20)),
                ('blueDefense4Crossings', models.IntegerField(default=-1)),
                ('blueDefense5Name', models.CharField(default=b'Unspecified', max_length=20)),
                ('blueDefense5Crossings', models.IntegerField(default=-1)),
                ('blueTowerFaceA', models.CharField(default=b'none', max_length=20)),
                ('blueTowerFaceB', models.CharField(default=b'none', max_length=20)),
                ('blueTowerFaceC', models.CharField(default=b'none', max_length=20)),
                ('blueFouls', models.IntegerField(default=-1)),
                ('blueTechFouls', models.IntegerField(default=-1)),
                ('audienceSelectionCategory', models.CharField(default=b'A', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='ScoreResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auto_defense', models.CharField(max_length=50)),
                ('auto_spy', models.CharField(max_length=50)),
                ('auto_score_low', models.IntegerField()),
                ('auto_score_high', models.IntegerField()),
                ('high_score_fail', models.IntegerField()),
                ('high_score_successful', models.IntegerField()),
                ('low_score_fail', models.IntegerField()),
                ('low_score_successful', models.IntegerField()),
                ('portcullis', models.IntegerField()),
                ('cheval_de_frise', models.IntegerField()),
                ('moat', models.IntegerField()),
                ('ramparts', models.IntegerField()),
                ('draw_bridge', models.IntegerField()),
                ('sally_port', models.IntegerField()),
                ('rock_wall', models.IntegerField()),
                ('rough_terrain', models.IntegerField()),
                ('low_bar', models.IntegerField()),
                ('slow_fast_portcullis', models.CharField(max_length=50)),
                ('slow_fast_cheval_de_frise', models.CharField(max_length=50)),
                ('slow_fast_moat', models.CharField(max_length=50)),
                ('slow_fast_ramparts', models.CharField(max_length=50)),
                ('slow_fast_draw_bridge', models.CharField(max_length=50)),
                ('slow_fast_sally_port', models.CharField(max_length=50)),
                ('slow_fast_rock_wall', models.CharField(max_length=50)),
                ('slow_fast_rough_terrain', models.CharField(max_length=50)),
                ('slow_fast_low_bar', models.CharField(max_length=50)),
                ('scale_challenge', models.CharField(max_length=50)),
                ('score_tech_foul', models.IntegerField()),
                ('notes_text_area', models.CharField(max_length=1000)),
                ('match', models.ForeignKey(to='Scouting2016.Match')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teamNumber', models.IntegerField()),
                ('homepage', models.CharField(max_length=1000)),
                ('teamOrganized', models.CharField(max_length=1000)),
                ('teamLikeable', models.CharField(max_length=1000)),
                ('teamSwag', models.CharField(max_length=1000)),
                ('teamAwards', models.CharField(max_length=1000)),
                ('teamAbilities', models.CharField(max_length=1000)),
                ('teamAlliances', models.CharField(max_length=1000)),
                ('teamAlly174', models.CharField(max_length=3)),
                ('teamOperational', models.CharField(max_length=3)),
                ('teamOperationProblems', models.CharField(max_length=1000)),
                ('teamFirstYear', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='TeamComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=1000)),
                ('team', models.ForeignKey(to='Scouting2016.Team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamPictures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=1000)),
                ('team', models.ForeignKey(to='Scouting2016.Team')),
            ],
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='team',
            field=models.ForeignKey(to='Scouting2016.Team'),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='blueTeam1',
            field=models.ForeignKey(related_name='blue1', to='Scouting2016.Team'),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='blueTeam2',
            field=models.ForeignKey(related_name='blue2', to='Scouting2016.Team'),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='blueTeam3',
            field=models.ForeignKey(related_name='blue3', to='Scouting2016.Team'),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redTeam1',
            field=models.ForeignKey(related_name='red1', to='Scouting2016.Team'),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redTeam2',
            field=models.ForeignKey(related_name='red2', to='Scouting2016.Team'),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redTeam3',
            field=models.ForeignKey(related_name='red3', to='Scouting2016.Team'),
        ),
    ]
