# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Scouting2013', '0002_auto_20170121_0010'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficialMatchScoreResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_score', models.IntegerField()),
                ('competition', models.ForeignKey(to='Scouting2013.Competition')),
                ('official_match', models.ForeignKey(to='Scouting2013.OfficialMatch')),
                ('team1', models.ForeignKey(related_name='team1', to='Scouting2013.Team')),
                ('team2', models.ForeignKey(related_name='team2', to='Scouting2013.Team')),
                ('team3', models.ForeignKey(related_name='team3', to='Scouting2013.Team')),
            ],
        ),
        migrations.CreateModel(
            name='PickList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grouping', models.CharField(max_length=1000)),
                ('rank_in_group', models.IntegerField(default=1)),
                ('competition', models.ForeignKey(to='Scouting2013.Competition')),
                ('team', models.ForeignKey(to='Scouting2013.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Scout2013',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bookmarked_teams', models.ManyToManyField(related_name='bookmarks', to='Scouting2013.Team')),
                ('do_not_pick_teams', models.ManyToManyField(related_name='do_not_picks', to='Scouting2013.Team')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamPitScouting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('team', models.OneToOneField(to='Scouting2013.Team')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='blue1',
            field=models.ForeignKey(related_name='blue1_matches', to='Scouting2013.Team', null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='blue2',
            field=models.ForeignKey(related_name='blue2_matches', to='Scouting2013.Team', null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='blue3',
            field=models.ForeignKey(related_name='blue3_matches', to='Scouting2013.Team', null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='red1',
            field=models.ForeignKey(related_name='red1_matches', to='Scouting2013.Team', null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='red2',
            field=models.ForeignKey(related_name='red2_matches', to='Scouting2013.Team', null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='red3',
            field=models.ForeignKey(related_name='red3_matches', to='Scouting2013.Team', null=True),
        ),
    ]
