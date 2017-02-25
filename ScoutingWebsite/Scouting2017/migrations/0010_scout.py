# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Scouting2017', '0009_auto_20170225_0116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bookmarked_teams', models.ManyToManyField(related_name='bookmarks', to='Scouting2017.Team')),
                ('do_not_pick_teams', models.ManyToManyField(related_name='do_not_picks', to='Scouting2017.Team')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
