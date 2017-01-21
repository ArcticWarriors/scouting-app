# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2015', '0003_auto_20160421_2311'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Compitition',
            new_name='Competition',
        ),
    ]
