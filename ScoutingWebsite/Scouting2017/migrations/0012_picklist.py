# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2017', '0011_auto_20170226_0102'),
    ]

    operations = [
        migrations.CreateModel(
            name='PickList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grouping', models.CharField(max_length=1000)),
                ('competition', models.ForeignKey(to='Scouting2017.Competition')),
                ('team', models.ForeignKey(to='Scouting2017.Team')),
            ],
        ),
    ]
