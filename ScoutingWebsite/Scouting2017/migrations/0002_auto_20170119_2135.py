# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2017', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoreresult',
            name='baseline',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='foul',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='fuel_score_hi',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='fuel_score_hi_auto',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='fuel_score_low',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='fuel_score_low_auto',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='fuel_shot_hi',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='fuel_shot_hi_auto',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='fuel_shot_low',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='fuel_shot_low_auto',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='gears_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='gears_score_auto',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='ground_fuel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='ground_gear',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='hopper',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='red_card',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='rope',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='tech_foul',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='yellow_card',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='teampitscouting',
            name='competent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='teampitscouting',
            name='short_fat',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='teampitscouting',
            name='tall_wide',
            field=models.BooleanField(default=False),
        ),
    ]
