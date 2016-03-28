# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0018_team_teamhomepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamPitScouting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bookmark', models.CharField(default=b'no', max_length=1000)),
                ('teamOrganized', models.CharField(max_length=1000)),
                ('teamLikeable', models.CharField(max_length=1000)),
                ('teamSwag', models.CharField(max_length=1000)),
                ('teamAwards', models.CharField(max_length=1000)),
                ('teamAlliances', models.CharField(default=b'no', max_length=1000)),
                ('drive', models.CharField(default=b'no', max_length=1000)),
                ('Auto', models.CharField(default=b'no', max_length=1000)),
                ('ScoreHigh', models.CharField(default=b'no', max_length=1000)),
                ('ScoreLow', models.CharField(default=b'no', max_length=1000)),
                ('portcullis', models.CharField(default=b'no', max_length=1000)),
                ('cheval', models.CharField(default=b'no', max_length=1000)),
                ('moat', models.CharField(default=b'no', max_length=1000)),
                ('ramparts', models.CharField(default=b'no', max_length=1000)),
                ('sally', models.CharField(default=b'no', max_length=1000)),
                ('drawbridge', models.CharField(default=b'no', max_length=1000)),
                ('rockwall', models.CharField(default=b'no', max_length=1000)),
                ('rough', models.CharField(default=b'no', max_length=1000)),
                ('lowBar', models.CharField(default=b'no', max_length=1000)),
                ('scale', models.CharField(default=b'no', max_length=1000)),
                ('teamAlly174', models.CharField(max_length=3)),
                ('teamOperational', models.CharField(max_length=3)),
                ('teamOperationProblems', models.CharField(max_length=1000)),
                ('team', models.ForeignKey(to='Scouting2016.Team')),
            ],
        ),
    ]
