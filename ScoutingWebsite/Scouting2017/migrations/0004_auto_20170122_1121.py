# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2017', '0003_auto_20170120_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='auto_baseline',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='auto_fuel_high',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='auto_fuel_low',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='auto_gears',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='fuel_high',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='fuel_low',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='takeoffs',
            field=models.IntegerField(default=0),
        ),
    ]
