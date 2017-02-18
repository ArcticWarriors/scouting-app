'''
Created on Jan 15, 2017

@author: PJ
'''
from django.db.models.aggregates import Avg, Sum
from django.db import models
from Scouting2017.model.reusable_models import Team, \
    OfficialMatch, Match, Competition, ScoreResultMetric



def get_team_metrics(team):
    metrics = team.scoreresult_set.aggregate(Avg("fuel_score_hi"),
                                             Avg("fuel_score_low"),
                                             Avg("fuel_score_hi_auto"),
                                             Avg("fuel_score_low_auto"),
                                             Avg("gears_score"),
                                             )
                                           
                                            
    # Format all of the numbers.  If we haven't scouted the team, None will be returned.  Turn that into NA
    for key in metrics:
        if metrics[key] == None:
            metrics[key] = "NA"
        elif "__avg" in key:
            metrics[key] = "{:10.2f}".format(metrics[key])

    return metrics


class TeamPitScouting(models.Model):

    team = models.OneToOneField(Team)
    
    competent = models.BooleanField(default=False)
    short_fat = models.BooleanField(default=False)
    tall_wide = models.BooleanField(default=False)

class OfficialMatchScoreResult(models.Model):

    official_match = models.ForeignKey(OfficialMatch)
    competition = models.ForeignKey(Competition)

    team1 = models.ForeignKey(Team, related_name='da_team1')
    team2 = models.ForeignKey(Team, related_name='da_team2')
    team3 = models.ForeignKey(Team, related_name='da_team3')
    
    robot1Auto = models.CharField(max_length=2000, default="")
    robot2Auto = models.CharField(max_length=2000, default="")
    robot3Auto = models.CharField(max_length=2000, default="")
    autoFuelLow = models.IntegerField(default=0)
    autoFuelHigh = models.IntegerField(default=0)
    rotor1Auto = models.IntegerField(default=0)
    rotor2Auto = models.IntegerField(default=0)
    teleopFuelLow = models.IntegerField(default=0)
    teleopFuelHigh = models.IntegerField(default=0)
    rotor1Engaged = models.IntegerField(default=0)
    rotor2Engaged = models.IntegerField(default=0)
    rotor3Engaged = models.IntegerField(default=0)
    rotor4Engaged = models.IntegerField(default=0)
    touchpadNear = models.IntegerField(default=0)
    touchpadMiddle = models.IntegerField(default=0)
    touchpadFar = models.IntegerField(default=0)
    foulCount = models.IntegerField(default=0)
    techFoulCount = models.IntegerField(default=0)
    autoMobilityPoints = models.IntegerField(default=0)
    autoRotorPoints = models.IntegerField(default=0)
    autoPoints = models.IntegerField(default=0)
    teleopFuelPoints = models.IntegerField(default=0)
    teleopRotorPoints = models.IntegerField(default=0)
    teleopTakeoffPoints = models.IntegerField(default=0)
    teleopPoints = models.IntegerField(default=0)
    foulPoints = models.IntegerField(default=0)
    totalPoints = models.IntegerField(default=0)
    kPaRankingPointAchieved = models.BooleanField(default=False)
    rotorRankingPointAchieved = models.BooleanField(default=False)


class ScoreResult(models.Model):

    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)
    competition = models.ForeignKey(Competition)
    
    # Teleop
    gears_score = models.IntegerField(default=0)
    fuel_shot_hi = models.IntegerField(default=0)
    fuel_shot_low = models.IntegerField(default=0)
    fuel_score_hi = models.IntegerField(default=0)
    fuel_score_low = models.IntegerField(default=0)
    rope = models.BooleanField(default=False)
    hopper = models.BooleanField(default=False)
#     defensive = models.BooleanField(default=False)
    
    # Fouls
    tech_foul = models.IntegerField(default=0)
    foul = models.IntegerField(default=0)
    red_card = models.BooleanField(default=False)
    yellow_card = models.BooleanField(default=False)
    
    # Auto
    fuel_shot_hi_auto = models.IntegerField(default=0)
    fuel_shot_low_auto = models.IntegerField(default=0)
    fuel_score_hi_auto = models.IntegerField(default=0)
    fuel_score_low_auto = models.IntegerField(default=0)
    gears_score_auto = models.IntegerField(default=0)
    baseline = models.BooleanField(default=False)
    scored_gear_in_auto = models.BooleanField(default=False)
    
    #collecting
    ground_fuel = models.BooleanField(default=False)
    ground_gear = models.BooleanField(default=False)
    #stats
    

    @staticmethod
    def get_fields():

        output = {}
        
        # Auto 
        
        # Fuel
        output['fuel_score_hi'] = ScoreResultMetric ('fuel_score_hi', 'High Fuel Scored', 0, "Average")
        output['fuel_score_low'] = ScoreResultMetric ('fuel_score_low', 'Low Fuel Scored', 0, "Average")
        output['gears_score'] = ScoreResultMetric ('gears_score', 'Gears Scored', 0, "Average")

        return output

    def __str__(self):
        output = "Score Result:\n"

        attributes = sorted(self.get_fields().keys())
        for attr_name in attributes:
            value = getattr(self, attr_name)
            output += "  {0:25} = {1}\n".format(attr_name, value)

        return output

