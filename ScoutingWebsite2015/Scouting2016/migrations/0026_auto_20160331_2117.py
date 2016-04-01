# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0025_remove_officialmatch_audienceselectioncategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='city',
            field=models.CharField(default=b'Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='team',
            name='country',
            field=models.CharField(default=b'Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='team',
            name='robot_name',
            field=models.CharField(default=b'Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='team',
            name='state',
            field=models.CharField(default=b'Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='team',
            name='team_name',
            field=models.CharField(default=b'Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='team',
            name='team_nickname',
            field=models.CharField(default=b'Unknown', max_length=100),
        ),
    ]
