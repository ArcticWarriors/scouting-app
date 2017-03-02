# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2011', '0002_auto_20170121_0010'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficialMatchScoreResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_score', models.IntegerField()),
                ('competition', models.ForeignKey(to='Scouting2011.Competition')),
                ('official_match', models.ForeignKey(to='Scouting2011.OfficialMatch')),
                ('team1', models.ForeignKey(related_name='team1', to='Scouting2011.Team')),
                ('team2', models.ForeignKey(related_name='team2', to='Scouting2011.Team')),
                ('team3', models.ForeignKey(related_name='team3', to='Scouting2011.Team')),
            ],
        ),
    ]
