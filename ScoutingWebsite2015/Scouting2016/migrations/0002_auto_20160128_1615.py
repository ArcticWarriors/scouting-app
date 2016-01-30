# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoreresult',
            name='auto_defense',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='auto_spy',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='portcullis',
            field=models.IntegerField(default=b''),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='scale_challenge',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='slow_fast_bridge',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='slow_fast_cheval',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='slow_fast_low_bar',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='slow_fast_moat',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='slow_fast_portculis',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='slow_fast_ramparts',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='slow_fast_rock_wall',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='slow_fast_rough',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='slow_fast_sally',
            field=models.CharField(default=b'', max_length=50),
        ),
    ]
