# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2017', '0010_scout'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoreresult',
            name='match_comments',
            field=models.CharField(default=b'', max_length=1000),
        ),
        migrations.AlterField(
            model_name='scoreresult',
            name='hoppers_dumped',
            field=models.IntegerField(default=0),
        ),
    ]
