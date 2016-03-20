# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0017_auto_20160320_0047'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='teamHomepage',
            field=models.CharField(default=b'', max_length=2000),
        ),
    ]
