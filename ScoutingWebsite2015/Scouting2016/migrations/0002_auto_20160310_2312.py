# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='officialmatch',
            name='blueTeleDefenseCrossings',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='officialmatch',
            name='redTeleDefenseCrossings',
            field=models.IntegerField(default=-1),
        ),
    ]
