# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0004_auto_20160128_1750'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scoreresult',
            old_name='slow_fast_portculis',
            new_name='slow_fast_portcullis',
        ),
    ]
