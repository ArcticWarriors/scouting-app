# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0031_officialmatch_competition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officialmatch',
            name='competition',
            field=models.ForeignKey(to='Scouting2016.Compitition'),
        ),
        migrations.AlterField(
            model_name='officialmatchscoreresult',
            name='competition',
            field=models.ForeignKey(to='Scouting2016.Compitition'),
        ),
        migrations.AlterField(
            model_name='scoreresult',
            name='competition',
            field=models.ForeignKey(to='Scouting2016.Compitition'),
        ),
        migrations.AlterField(
            model_name='team',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='team',
            name='country',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='team',
            name='robot_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='team',
            name='state',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_nickname',
            field=models.CharField(max_length=100),
        ),
    ]
