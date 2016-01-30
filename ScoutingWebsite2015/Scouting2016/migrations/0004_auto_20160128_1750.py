# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0003_auto_20160128_1617'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scoreresult',
            name='match_number',
        ),
        migrations.RemoveField(
            model_name='scoreresult',
            name='team_number',
        ),
    ]
