'''
Created on Mar 28, 2015

@author: PJ
'''
from django.db import models
from Scouting2015.model.reusable_models import Team, OfficialMatch, Competition


class OfficialMatchScoreResult(models.Model):

    official_match = models.ForeignKey(OfficialMatch)
    competition = models.ForeignKey(Competition)

    team1 = models.ForeignKey(Team, related_name='da_team1')
    team2 = models.ForeignKey(Team, related_name='da_team2')
    team3 = models.ForeignKey(Team, related_name='da_team3')

    # Auton
    auton_robot_set = models.BooleanField(default=False)
    auton_tote_set = models.BooleanField(default=False)
    auton_tote_stack = models.BooleanField(default=False)
    auton_container_set = models.BooleanField(default=False)

    # Totes
    totes_on_close_platform = models.IntegerField(default=-1)
    totes_on_far_platform = models.IntegerField(default=-1)

    # Containers (# on top of N totes)
    containers_on_level_1 = models.IntegerField(default=-1)
    containers_on_level_2 = models.IntegerField(default=-1)
    containers_on_level_3 = models.IntegerField(default=-1)
    containers_on_level_4 = models.IntegerField(default=-1)
    containers_on_level_5 = models.IntegerField(default=-1)
    containers_on_level_6 = models.IntegerField(default=-1)

    def predict(self):
        return 123
