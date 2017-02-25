# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2017', '0008_auto_20170224_0137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scoreresult',
            old_name='baseline',
            new_name='auto_baseline',
        ),
        migrations.RenameField(
            model_name='scoreresult',
            old_name='fuel_score_hi_auto',
            new_name='auto_fuel_high_score',
        ),
        migrations.RenameField(
            model_name='scoreresult',
            old_name='fuel_shot_hi_auto',
            new_name='auto_fuel_high_shots',
        ),
        migrations.RenameField(
            model_name='scoreresult',
            old_name='fuel_score_low_auto',
            new_name='auto_fuel_low_score',
        ),
        migrations.RenameField(
            model_name='scoreresult',
            old_name='fuel_shot_low_auto',
            new_name='auto_fuel_low_shots',
        ),
        migrations.RenameField(
            model_name='scoreresult',
            old_name='gears_score_auto',
            new_name='auto_gears',
        ),
        migrations.RenameField(
            model_name='scoreresult',
            old_name='ground_fuel',
            new_name='gathered_fuel_from_ground',
        ),
        migrations.RenameField(
            model_name='scoreresult',
            old_name='ground_gear',
            new_name='gathered_gear_from_ground',
        ),
        migrations.RenameField(
            model_name='scoreresult',
            old_name='hopper',
            new_name='hoppers_dumped',
        ),
        migrations.RenameField(
            model_name='scoreresult',
            old_name='fuel_score_hi',
            new_name='tele_fuel_high_score',
        ),
        migrations.RenameField(
            model_name='scoreresult',
            old_name='fuel_shot_hi',
            new_name='tele_fuel_high_shots',
        ),
        migrations.RenameField(
            model_name='scoreresult',
            old_name='fuel_score_low',
            new_name='tele_fuel_low_score',
        ),
        migrations.RenameField(
            model_name='scoreresult',
            old_name='fuel_shot_low',
            new_name='tele_fuel_low_shots',
        ),
        migrations.RenameField(
            model_name='scoreresult',
            old_name='gears_score',
            new_name='tele_gears',
        ),
    ]
