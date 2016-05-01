# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2015', '0002_auto_20160421_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='auton_container_set',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='auton_robot_set',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='auton_tote_set',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='auton_tote_stack',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='containers_on_level_1',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='containers_on_level_2',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='containers_on_level_3',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='containers_on_level_4',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='containers_on_level_5',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='containers_on_level_6',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='totes_on_close_platform',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='totes_on_far_platform',
            field=models.IntegerField(default=-1),
        ),
    ]
