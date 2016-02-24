# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0007_officialmatch'),
    ]

    operations = [
        migrations.AddField(
            model_name='officialmatch',
            name='audienceSelectionCategory',
            field=models.CharField(default=b'A', max_length=1),
        ),
    ]
