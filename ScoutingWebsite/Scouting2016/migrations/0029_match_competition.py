# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0028_auto_20160331_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='competition',
            field=models.ForeignKey(default=399, to='Scouting2016.Compitition'),
        ),
    ]
