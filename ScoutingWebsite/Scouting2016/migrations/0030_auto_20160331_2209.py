# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2016', '0029_match_competition'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamCompetesIn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('competition', models.ForeignKey(to='Scouting2016.Compitition')),
                ('team', models.ForeignKey(to='Scouting2016.Team')),
            ],
        ),
        migrations.AddField(
            model_name='officialmatchscoreresult',
            name='competition',
            field=models.ForeignKey(default=399, to='Scouting2016.Compitition'),
        ),
        migrations.AddField(
            model_name='scoreresult',
            name='competition',
            field=models.ForeignKey(default=399, to='Scouting2016.Compitition'),
        ),
        migrations.AlterField(
            model_name='match',
            name='competition',
            field=models.ForeignKey(to='Scouting2016.Compitition'),
        ),
    ]
