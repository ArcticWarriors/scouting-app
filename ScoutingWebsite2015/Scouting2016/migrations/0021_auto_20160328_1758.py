# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0020_auto_20160328_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='teamHomepage',
            new_name='homepage',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='teamFirstYear',
            new_name='rookie_year',
        ),
    ]
