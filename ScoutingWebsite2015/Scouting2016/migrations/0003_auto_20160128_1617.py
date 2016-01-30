# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0002_auto_20160128_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoreresult',
            name='portcullis',
            field=models.IntegerField(default=0),
        ),
    ]
