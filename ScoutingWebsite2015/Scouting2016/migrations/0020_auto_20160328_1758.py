# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0019_teampitscouting'),
    ]

    operations = [
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
        migrations.AlterField(
            model_name='team',
            name='teamFirstYear',
            field=models.CharField(max_length=4),
        ),
    ]
