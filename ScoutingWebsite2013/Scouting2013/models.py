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


class ScoreResult(models.Model):

    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)

    auton_score = models.IntegerField()
    pyramid_goals = models.IntegerField()
    high_goals = models.IntegerField()
    mid_goals = models.IntegerField()
    low_goals = models.IntegerField()
    missed_shots = models.IntegerField()
    invalid_hangs = models.IntegerField()
    hanging_points = models.IntegerField()
    fouls = models.IntegerField()
    technical_fouls = models.IntegerField()
    yellow_card = models.BooleanField()
    red_card = models.BooleanField()
    broke_badly = models.BooleanField()
