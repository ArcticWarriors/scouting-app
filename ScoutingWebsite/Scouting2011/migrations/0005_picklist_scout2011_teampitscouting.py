# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Scouting2011', '0004_auto_20170302_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='PickList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grouping', models.CharField(max_length=1000)),
                ('rank_in_group', models.IntegerField(default=1)),
                ('competition', models.ForeignKey(to='Scouting2011.Competition')),
                ('team', models.ForeignKey(to='Scouting2011.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Scout2011',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bookmarked_teams', models.ManyToManyField(related_name='bookmarks', to='Scouting2011.Team')),
                ('do_not_pick_teams', models.ManyToManyField(related_name='do_not_picks', to='Scouting2011.Team')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamPitScouting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('team', models.OneToOneField(to='Scouting2011.Team')),
            ],
        ),
    ]
