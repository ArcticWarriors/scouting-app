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
                ('team_number', models.IntegerField()),
                ('match_number', models.IntegerField()),
                ('auto_score_low', models.IntegerField()),
                ('auto_score_high', models.IntegerField()),
                ('cheval_de_frise', models.IntegerField()),
                ('ramparts', models.IntegerField()),
                ('sally_port', models.IntegerField()),
                ('low_bar', models.IntegerField()),
                ('rock_wall', models.IntegerField()),
                ('draw_bridge', models.IntegerField()),
                ('moat', models.IntegerField()),
                ('rough_terrain', models.IntegerField()),
                ('score_tech_foul', models.IntegerField()),
                ('high_score_fail', models.IntegerField()),
                ('high_score_successful', models.IntegerField()),
                ('low_score_successful', models.IntegerField()),
                ('low_score_fail', models.IntegerField()),
                ('notes_text_area', models.CharField(max_length=1000)),
                ('match', models.ForeignKey(to='Scouting2016.Match')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teamNumber', models.IntegerField()),
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
        migrations.AddField(
            model_name='scoreresult',
            name='team',
            field=models.ForeignKey(to='Scouting2016.Team'),
        ),
    ]
