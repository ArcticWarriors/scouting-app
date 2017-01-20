'''
Created on Mar 28, 2016

@author: PJ
'''
from django.db import models


class ScoreResultMetric:

    def __init__(self, field_name, display_name, default, metric_type=None):
        self.field_name = field_name
        self.display_name = display_name
        self.default = default
        self.metric_type = metric_type

    def __str__(self):
        return "SRMetric: [%s, %s, %s, %s]" % (self.field_name, self.display_name, self.default, self.metric_type)


class Competition(models.Model):

    code = models.CharField(max_length=6)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return "Competition %s - %s" % (self.code, self.name)


class Match(models.Model):

    matchNumber = models.IntegerField()
    competition = models.ForeignKey(Competition)

    def __str__(self):
        return "Match %s at Competitions %s" % (self.matchNumber, self.competition)


class Team(models.Model):

    teamNumber = models.IntegerField()
    homepage = models.CharField(max_length=2000, default="")
    rookie_year = models.CharField(max_length=4)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    team_name = models.CharField(max_length=100)
    team_nickname = models.CharField(max_length=100)
    robot_name = models.CharField(max_length=100)

    def __str__(self):
        return "Team %s" % self.teamNumber


class TeamCompetesIn(models.Model):
    team = models.ForeignKey(Team)
    competition = models.ForeignKey(Competition)


class TeamComments(models.Model):

    comment = models.CharField(max_length=1000)

    team = models.ForeignKey(Team)


class TeamPictures(models.Model):

    path = models.CharField(max_length=1000)

    team = models.ForeignKey(Team)


class OfficialMatch(models.Model):

    matchNumber = models.IntegerField()
    competition = models.ForeignKey(Competition)

    hasOfficialData = models.BooleanField(default=False)
