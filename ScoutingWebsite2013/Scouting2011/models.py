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

    TubesDropped      = models.IntegerField()
    LowTubesHung      = models.IntegerField()
    MidTubesHung      = models.IntegerField()
    HighTubesHung     = models.IntegerField()
    TubesRecieved     = models.IntegerField()
    Penelties         = models.IntegerField()
    MiniBotFinish     = models.IntegerField()
    DeployedMinibot   = models.BooleanField()
    ScoredUberTube    = models.BooleanField()
    WasOffensive      = models.BooleanField()
    WasScouted        = models.BooleanField()
    BrokeBadly        = models.BooleanField()
    Comments          = models.CharField(max_length=1000)
