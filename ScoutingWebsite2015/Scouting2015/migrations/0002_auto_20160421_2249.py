# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2015', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='autoBouldersHigh',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='autoBouldersLow',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='autonA',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='autonB',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='autonC',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='defense1Crossings',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='defense2Crossings',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='defense2Name',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='defense3Crossings',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='defense3Name',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='defense4Crossings',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='defense4Name',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='defense5Crossings',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='defense5Name',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='fouls',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='techFouls',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='teleBouldersHigh',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='teleBouldersLow',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='teleDefenseCrossings',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='towerFaceA',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='towerFaceB',
        ),
        migrations.RemoveField(
            model_name='officialmatchscoreresult',
            name='towerFaceC',
        ),
    ]
