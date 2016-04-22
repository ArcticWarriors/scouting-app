'''
Created on Mar 28, 2015

@author: PJ
'''
from django.db.models.aggregates import Avg, Sum
from django.db import models
from Scouting2015.model.reusable_models import ScoreResultMetric, Team, \
    OfficialMatch, Match, Compitition


class OfficialMatchScoreResult(models.Model):

    official_match = models.ForeignKey(OfficialMatch)
    competition = models.ForeignKey(Compitition)

    team1 = models.ForeignKey(Team, related_name='da_team1')
    team2 = models.ForeignKey(Team, related_name='da_team2')
    team3 = models.ForeignKey(Team, related_name='da_team3')

    def predict(self):
        return 123

