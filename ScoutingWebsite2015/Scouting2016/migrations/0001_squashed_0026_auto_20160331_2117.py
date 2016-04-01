# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [(b'Scouting2016', '0001_initial'), (b'Scouting2016', '0002_auto_20160310_2312'), (b'Scouting2016', '0003_auto_20160312_1100'), (b'Scouting2016', '0004_auto_20160312_1100'), (b'Scouting2016', '0005_auto_20160319_1850'), (b'Scouting2016', '0006_remove_team_homepage'), (b'Scouting2016', '0007_remove_team_teamally174'), (b'Scouting2016', '0008_team_teamally174'), (b'Scouting2016', '0009_auto_20160319_2143'), (b'Scouting2016', '0010_team_teamalliances'), (b'Scouting2016', '0011_auto_20160319_2205'), (b'Scouting2016', '0012_team_bookmark'), (b'Scouting2016', '0013_auto_20160319_2318'), (b'Scouting2016', '0014_auto_20160319_2319'), (b'Scouting2016', '0015_auto_20160319_2358'), (b'Scouting2016', '0016_auto_20160320_0044'), (b'Scouting2016', '0017_auto_20160320_0047'), (b'Scouting2016', '0018_team_teamhomepage'), (b'Scouting2016', '0019_teampitscouting'), (b'Scouting2016', '0020_auto_20160328_1758'), (b'Scouting2016', '0021_auto_20160328_1758'), (b'Scouting2016', '0022_officialmatchscoreresult'), (b'Scouting2016', '0023_auto_20160328_1809'), (b'Scouting2016', '0024_auto_20160328_1812'), (b'Scouting2016', '0025_remove_officialmatch_audienceselectioncategory'), (b'Scouting2016', '0026_auto_20160331_2117')]

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
        migrations.AddField(
            model_name='officialmatch',
            name='blueTeleDefenseCrossings',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redTeleDefenseCrossings',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redAutonA',
            field=models.CharField(default=b'None', max_length=20),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redAutonB',
            field=models.CharField(default=b'None', max_length=20),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redAutonC',
            field=models.CharField(default=b'None', max_length=20),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='blueAutonA',
            field=models.CharField(default=b'None', max_length=20),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='blueAutonB',
            field=models.CharField(default=b'None', max_length=20),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='blueAutonC',
            field=models.CharField(default=b'None', max_length=20),
        ),
        migrations.RemoveField(
            model_name='team',
            name='teamAbilities',
        ),
        migrations.RemoveField(
            model_name='team',
            name='teamAlliances',
        ),
        migrations.RemoveField(
            model_name='team',
            name='homepage',
        ),
        migrations.RemoveField(
            model_name='team',
            name='teamAlly174',
        ),
        migrations.AddField(
            model_name='team',
            name='teamAlly174',
            field=models.CharField(default=2, max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='Auto',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='ScoreHigh',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='ScoreLow',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='cheval',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='drawbridge',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='drive',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='lowBar',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='moat',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='portcullis',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='ramparts',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='rockwall',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='rough',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='sally',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='scale',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='teamAlliances',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='bookmark',
            field=models.CharField(default=b'no', max_length=1000),
        ),
        migrations.AddField(
            model_name='team',
            name='teamHomepage',
            field=models.CharField(default=b'', max_length=2000),
        ),
        migrations.CreateModel(
            name='TeamPitScouting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bookmark', models.CharField(default=b'no', max_length=1000)),
                ('teamOrganized', models.CharField(max_length=1000)),
                ('teamLikeable', models.CharField(max_length=1000)),
                ('teamSwag', models.CharField(max_length=1000)),
                ('teamAwards', models.CharField(max_length=1000)),
                ('teamAlliances', models.CharField(default=b'no', max_length=1000)),
                ('drive', models.CharField(default=b'no', max_length=1000)),
                ('Auto', models.CharField(default=b'no', max_length=1000)),
                ('ScoreHigh', models.CharField(default=b'no', max_length=1000)),
                ('ScoreLow', models.CharField(default=b'no', max_length=1000)),
                ('portcullis', models.CharField(default=b'no', max_length=1000)),
                ('cheval', models.CharField(default=b'no', max_length=1000)),
                ('moat', models.CharField(default=b'no', max_length=1000)),
                ('ramparts', models.CharField(default=b'no', max_length=1000)),
                ('sally', models.CharField(default=b'no', max_length=1000)),
                ('drawbridge', models.CharField(default=b'no', max_length=1000)),
                ('rockwall', models.CharField(default=b'no', max_length=1000)),
                ('rough', models.CharField(default=b'no', max_length=1000)),
                ('lowBar', models.CharField(default=b'no', max_length=1000)),
                ('scale', models.CharField(default=b'no', max_length=1000)),
                ('teamAlly174', models.CharField(max_length=3)),
                ('teamOperational', models.CharField(max_length=3)),
                ('teamOperationProblems', models.CharField(max_length=1000)),
                ('team', models.OneToOneField(to='Scouting2016.Team')),
            ],
        ),
        migrations.RemoveField(
            model_name='team',
            name='Auto',
        ),
        migrations.RemoveField(
            model_name='team',
            name='ScoreHigh',
        ),
        migrations.RemoveField(
            model_name='team',
            name='ScoreLow',
        ),
        migrations.RemoveField(
            model_name='team',
            name='bookmark',
        ),
        migrations.RemoveField(
            model_name='team',
            name='cheval',
        ),
        migrations.RemoveField(
            model_name='team',
            name='drawbridge',
        ),
        migrations.RemoveField(
            model_name='team',
            name='drive',
        ),
        migrations.RemoveField(
            model_name='team',
            name='lowBar',
        ),
        migrations.RemoveField(
            model_name='team',
            name='moat',
        ),
        migrations.RemoveField(
            model_name='team',
            name='portcullis',
        ),
        migrations.RemoveField(
            model_name='team',
            name='ramparts',
        ),
        migrations.RemoveField(
            model_name='team',
            name='rockwall',
        ),
        migrations.RemoveField(
            model_name='team',
            name='rough',
        ),
        migrations.RemoveField(
            model_name='team',
            name='sally',
        ),
        migrations.RemoveField(
            model_name='team',
            name='scale',
        ),
        migrations.RemoveField(
            model_name='team',
            name='teamAlliances',
        ),
        migrations.RemoveField(
            model_name='team',
            name='teamAlly174',
        ),
        migrations.RemoveField(
            model_name='team',
            name='teamAwards',
        ),
        migrations.RemoveField(
            model_name='team',
            name='teamLikeable',
        ),
        migrations.RemoveField(
            model_name='team',
            name='teamOperationProblems',
        ),
        migrations.RemoveField(
            model_name='team',
            name='teamOperational',
        ),
        migrations.RemoveField(
            model_name='team',
            name='teamOrganized',
        ),
        migrations.RemoveField(
            model_name='team',
            name='teamSwag',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='teamFirstYear',
            new_name='rookie_year',
        ),
        migrations.AlterField(
            model_name='team',
            name='rookie_year',
            field=models.CharField(max_length=4),
        ),
        migrations.RenameField(
            model_name='team',
            old_name='teamHomepage',
            new_name='homepage',
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
                ('official_match', models.ForeignKey(to='Scouting2016.OfficialMatch')),
                ('team1', models.ForeignKey(related_name='da_team1', to='Scouting2016.Team')),
                ('team2', models.ForeignKey(related_name='da_team2', to='Scouting2016.Team')),
                ('team3', models.ForeignKey(related_name='da_team3', to='Scouting2016.Team')),
            ],
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueAutoBouldersHigh',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueAutoBouldersLow',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueAutonA',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueAutonB',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueAutonC',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueDefense1Crossings',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueDefense2Crossings',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueDefense2Name',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueDefense3Crossings',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueDefense3Name',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueDefense4Crossings',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueDefense4Name',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueDefense5Crossings',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueDefense5Name',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueFouls',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueTeam1',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueTeam2',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueTeam3',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueTechFouls',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueTeleBouldersHigh',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueTeleBouldersLow',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueTeleDefenseCrossings',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueTowerFaceA',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueTowerFaceB',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueTowerFaceC',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redAutoBouldersHigh',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redAutoBouldersLow',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redAutonA',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redAutonB',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redAutonC',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redDefense1Crossings',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redDefense2Crossings',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redDefense2Name',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redDefense3Crossings',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redDefense3Name',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redDefense4Crossings',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redDefense4Name',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redDefense5Crossings',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redDefense5Name',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redFouls',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redTeam1',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redTeam2',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redTeam3',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redTechFouls',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redTeleBouldersHigh',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redTeleBouldersLow',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redTeleDefenseCrossings',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redTowerFaceA',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redTowerFaceB',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redTowerFaceC',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='audienceSelectionCategory',
        ),
        migrations.AddField(
            model_name='team',
            name='city',
            field=models.CharField(default=b'Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='team',
            name='country',
            field=models.CharField(default=b'Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='team',
            name='robot_name',
            field=models.CharField(default=b'Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='team',
            name='state',
            field=models.CharField(default=b'Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='team',
            name='team_name',
            field=models.CharField(default=b'Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='team',
            name='team_nickname',
            field=models.CharField(default=b'Unknown', max_length=100),
        ),
    ]
