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
                ('auton_score', models.IntegerField()),
                ('pyramid_goals', models.IntegerField()),
                ('high_goals', models.IntegerField()),
                ('mid_goals', models.IntegerField()),
                ('low_goals', models.IntegerField()),
                ('missed_shots', models.IntegerField()),
                ('invalid_hangs', models.IntegerField()),
                ('hanging_points', models.IntegerField()),
                ('fouls', models.IntegerField()),
                ('technical_fouls', models.IntegerField()),
                ('yellow_card', models.BooleanField()),
                ('red_card', models.BooleanField()),
                ('broke_badly', models.BooleanField()),
                ('match', models.ForeignKey(to='Scouting2013.Match')),
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
            field=models.ForeignKey(to='Scouting2013.Team'),
        ),
    ]
