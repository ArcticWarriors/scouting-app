# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2017', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scout',
            name='team',
            field=models.ForeignKey(default=174, to='Scouting2017.Team'),
            preserve_default=False,
        ),
    ]
