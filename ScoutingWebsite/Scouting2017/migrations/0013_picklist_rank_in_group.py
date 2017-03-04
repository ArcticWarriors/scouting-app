# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2017', '0012_picklist'),
    ]

    operations = [
        migrations.AddField(
            model_name='picklist',
            name='rank_in_group',
            field=models.IntegerField(default=1),
        ),
    ]
