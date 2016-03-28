# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0023_auto_20160328_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teampitscouting',
            name='team',
            field=models.OneToOneField(to='Scouting2016.Team'),
        ),
    ]
