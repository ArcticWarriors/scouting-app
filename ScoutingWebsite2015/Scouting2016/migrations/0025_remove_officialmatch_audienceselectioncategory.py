# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0024_auto_20160328_1812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='officialmatch',
            name='audienceSelectionCategory',
        ),
    ]
