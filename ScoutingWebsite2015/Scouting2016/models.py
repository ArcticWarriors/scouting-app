from django.db import models

# Create your models here.

class Match(models.Model):

    matchNumber = models.IntegerField()

    def __str__(self):
        return "Match %s" % self.matchNumber


class Team(models.Model):

    teamNumber = models.IntegerField()

    def __str__(self):
        return "Team %s" % self.teamNumber

class TeamComments(models.Model):
    
    comment = models.CharField(max_length=1000)
    
    team = models.ForeignKey(Team)
    
class ScoreResult(models.Model):
    
    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)
    
    team_number = models.IntegerField()
    match_number = models.IntegerField()
    
    auto_score_low = models.IntegerField()
    auto_score_high = models.IntegerField()
    
    cheval_de_frise = models.IntegerField()
    ramparts = models.IntegerField()
    sally_port = models.IntegerField()
    low_bar = models.IntegerField()
    rock_wall = models.IntegerField()
    draw_bridge = models.IntegerField()
    moat = models.IntegerField()
    rough_terrain = models.IntegerField()
    
    score_tech_foul = models.IntegerField()
    
    high_score_fail = models.IntegerField()
    high_score_successful = models.IntegerField()
    low_score_successful = models.IntegerField()
    low_score_fail = models.IntegerField()
    
    notes_text_area =models.CharField(max_length=1000)
    
    