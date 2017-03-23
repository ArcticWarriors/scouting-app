'''
Created on Jan 15, 2017

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
    location = models.CharField(max_length=100)
    week = models.IntegerField(default=-1)

    def __str__(self):
        return "Competition %s - %s" % (self.code, self.name)


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


class Match(models.Model):

    matchNumber = models.IntegerField()
    competition = models.ForeignKey(Competition)
    red1 = models.ForeignKey(Team, related_name='red1')
    red2 = models.ForeignKey(Team, related_name='red2')
    red3 = models.ForeignKey(Team, related_name='red3')
    blue1 = models.ForeignKey(Team, related_name='blue1')
    blue2 = models.ForeignKey(Team, related_name='blue2')
    blue3 = models.ForeignKey(Team, related_name='blue3')

    def __str__(self):
        return "Match %s at Competitions %s" % (self.matchNumber, self.competition)


class TeamCompetesIn(models.Model):
    team = models.ForeignKey(Team)
    competition = models.ForeignKey(Competition)


class PickList(models.Model):

    competition = models.ForeignKey(Competition)
    team = models.ForeignKey(Team)
    grouping = models.CharField(max_length=1000)
    rank_in_group = models.IntegerField(default=1)


class TeamComments(models.Model):

    comment = models.CharField(max_length=1000)

    team = models.ForeignKey(Team)


class TeamPictures(models.Model):

    path = models.CharField(max_length=1000)

    team = models.ForeignKey(Team)

    def __str__(self):

        return "%s - %s" % (self.team, self.path)


class OfficialMatch(models.Model):

    matchNumber = models.IntegerField()
    competition = models.ForeignKey(Competition)

    hasOfficialData = models.BooleanField(default=False)
