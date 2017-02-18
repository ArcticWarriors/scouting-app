# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2017', '0004_auto_20170122_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='auto_baseline',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='auto_fuel_high',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='auto_fuel_low',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='auto_gears',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='fuel_high',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='fuel_low',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='takeoffs',
        ),
    ]
