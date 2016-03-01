# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0009_PitScouting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='officialmatch',
            name='blueScore',
        ),
        migrations.RemoveField(
            model_name='officialmatch',
            name='redScore',
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='blueAutoBouldersHigh',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='blueAutoBouldersLow',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='blueFouls',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='blueTechFouls',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='blueTeleBouldersHigh',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='blueTeleBouldersLow',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='blueTowerFaceA',
            field=models.CharField(default=b'none', max_length=20),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='blueTowerFaceB',
            field=models.CharField(default=b'none', max_length=20),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='blueTowerFaceC',
            field=models.CharField(default=b'none', max_length=20),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redAutoBouldersHigh',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redAutoBouldersLow',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redFouls',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redTechFouls',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redTeleBouldersHigh',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redTeleBouldersLow',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redTowerFaceA',
            field=models.CharField(default=b'none', max_length=20),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redTowerFaceB',
            field=models.CharField(default=b'none', max_length=20),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redTowerFaceC',
            field=models.CharField(default=b'none', max_length=20),
        ),
    ]
