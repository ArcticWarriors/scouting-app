'''
Created on Jan 15, 2017

@author: PJ
'''
from django.db.models.aggregates import Avg, Sum
from django.db import models
from Scouting2017.model.reusable_models import Team, \
    OfficialMatch, Match, Compitition



def get_team_metrics(team):
    metrics = team.scoreresult_set.aggregate()

    # Format all of the numbers.  If we haven't scouted the team, None will be returned.  Turn that into NA
    for key in metrics:
        if metrics[key] == None:
            metrics[key] = "NA"
        elif "__avg" in key:
            metrics[key] = "{:10.2f}".format(metrics[key])

    return metrics


class TeamPitScouting(models.Model):

    team = models.OneToOneField(Team)
    
    competent = models.BooleanField()
    short_fat = models.BooleanField()
    tall_wide = models.BooleanField()

class OfficialMatchScoreResult(models.Model):

    official_match = models.ForeignKey(OfficialMatch)
    competition = models.ForeignKey(Compitition)

    team1 = models.ForeignKey(Team, related_name='da_team1')
    team2 = models.ForeignKey(Team, related_name='da_team2')
    team3 = models.ForeignKey(Team, related_name='da_team3')


class ScoreResult(models.Model):

    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)
    competition = models.ForeignKey(Compitition)
    
    # Teleop
    gears_score = models.IntegerField()
    fuel_shot_hi = models.IntegerField()
    fuel_shot_low = models.IntegerField()
    fuel_score_hi = models.IntegerField()
    fuel_score_low = models.IntegerField()
    rope = models.BooleanField()
    hopper = models.BooleanField()
    
    # Fouls
    tech_foul = models.IntegerField()
    foul = models.IntegerField()
    red_card = models.BooleanField()
    yellow_card = models.BooleanField()
    
    # Auto
    fuel_shot_hi_auto = models.IntegerField()
    fuel_shot_low_auto = models.IntegerField()
    fuel_score_hi_auto = models.IntegerField()
    fuel_score_low_auto = models.IntegerField()
    gears_score_auto = models.IntegerField()
    baseline = models.BooleanField()
    
    #collecting
    ground_fuel = models.BooleanField()
    ground_gear = models.BooleanField()
    

    @staticmethod
    def get_fields():

        output = {}

        return output

    def __str__(self):
        output = "Score Result:\n"

        attributes = sorted(self.get_fields().keys())
        for attr_name in attributes:
            value = getattr(self, attr_name)
            output += "  {0:25} = {1}\n".format(attr_name, value)

        return output

