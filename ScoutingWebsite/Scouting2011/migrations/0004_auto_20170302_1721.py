# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scouting2011', '0003_officialmatchscoreresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='blue1',
            field=models.ForeignKey(related_name='blue1_matches', to='Scouting2011.Team', null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='blue2',
            field=models.ForeignKey(related_name='blue2_matches', to='Scouting2011.Team', null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='blue3',
            field=models.ForeignKey(related_name='blue3_matches', to='Scouting2011.Team', null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='red1',
            field=models.ForeignKey(related_name='red1_matches', to='Scouting2011.Team', null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='red2',
            field=models.ForeignKey(related_name='red2_matches', to='Scouting2011.Team', null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='red3',
            field=models.ForeignKey(related_name='red3_matches', to='Scouting2011.Team', null=True),
        ),
    ]
