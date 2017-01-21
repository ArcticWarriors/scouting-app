# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0032_auto_20160421_2234'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Compitition',
            new_name='Competition',
        ),
    ]
