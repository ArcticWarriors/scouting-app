'''
Created on Jan 15, 2017

@author: PJ
'''
from django.db.models.aggregates import Avg, Sum
from django.db import models
from Scouting2017.model.reusable_models import Team, \
    OfficialMatch, Match, Competition, ScoreResultMetric
from django.db.models.expressions import Case, When



def get_team_metrics(team):
    metrics = team.scoreresult_set.aggregate(Avg("auto_fuel_high_score"),
                                             Avg("auto_fuel_high_shots"),
                                             Avg("auto_fuel_low_score"),
                                             Avg("auto_fuel_low_shots"),
                                             Avg("auto_gears"),
                                             
                                             Avg("tele_fuel_high_score"),
                                             Avg("tele_fuel_high_shots"),
                                             Avg("tele_fuel_low_score"),
                                             Avg("tele_fuel_low_shots"),
                                             Avg("tele_gears"),
                                             
                                             Sum("foul"),
                                             Sum("tech_foul"),
                                             Sum("yellow_card"),
                                             Sum("red_card"),
                                             
                                             rope__avg = Avg(Case(When(rope=True, then=1),When(rope=False, then=0))),
                                             baseline__avg=Avg(Case(When(auto_baseline=True, then=1),When(auto_baseline=False, then=0))),
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

    OrganizedFunctional = models.CharField(max_length=1000, default="no")
    FuelCapacity = models.CharField(max_length=1000, default="no")
    Gears = models.CharField(max_length=1000, default="no")
    Strategy = models.CharField(max_length=1000)
    Size = models.CharField(max_length=1000)
    FuelAcquire = models.CharField(max_length=1000)
    AllianceStrategy  = models.CharField(max_length=1000, default="no")
    AllanceCompetent = models.CharField(max_length=1000, default="no")
    CompetnetConfident = models.CharField(max_length=1000, default="no")
    Competitions = models.CharField(max_length=1000, default="no")
    Random = models.CharField(max_length=1000)


class OfficialMatchScoreResult(models.Model):

    official_match = models.ForeignKey(OfficialMatch)
    competition = models.ForeignKey(Competition)
    
    alliance_color = models.CharField(max_length=1, choices=(('R', 'Red'), ('B', 'Blue')))
    
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
    
    # Auto
    auto_gears = models.IntegerField(default=0)
    auto_fuel_high_shots = models.IntegerField(default=0)
    auto_fuel_high_score = models.IntegerField(default=0)
    auto_fuel_low_shots = models.IntegerField(default=0)
    auto_fuel_low_score = models.IntegerField(default=0)
    auto_baseline = models.BooleanField(default=False)
    
    # Teleop
    tele_gears = models.IntegerField(default=0)
    tele_fuel_high_shots = models.IntegerField(default=0)
    tele_fuel_high_score = models.IntegerField(default=0)
    tele_fuel_low_shots = models.IntegerField(default=0)
    tele_fuel_low_score = models.IntegerField(default=0)
    
    # Endgame
    rope = models.BooleanField(default=False)
    
    
    # Fouls
    tech_foul = models.IntegerField(default=0)
    foul = models.IntegerField(default=0)
    red_card = models.BooleanField(default=False)
    yellow_card = models.BooleanField(default=False)
    
    #collecting
    hoppers_dumped = models.IntegerField(default=0)
    gathered_fuel_from_ground = models.BooleanField(default=False)
    gathered_gear_from_ground = models.BooleanField(default=False)
    
    match_comments = models.CharField(max_length=1000, default="")
    

    @staticmethod
    def get_fields():

        output = {}

        return output

    def __str__(self):
        output = "Score Result:{"

        attributes = sorted(self.get_fields().keys())
        for attr_name in attributes:
            value = getattr(self, attr_name)
            output += "{0}: {1}".format(attr_name, value)
            
        output += "}"

        return output

