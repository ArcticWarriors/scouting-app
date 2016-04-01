# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0027_event'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Event',
            new_name='Compitition',
        ),
    ]
