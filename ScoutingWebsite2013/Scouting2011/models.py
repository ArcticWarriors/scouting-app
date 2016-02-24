from django.db import models
from django.db.models import Avg, Sum


class ScoreResultMetric:

    def __init__(self, field_name, display_name, default, metric_type=None):
        self.field_name = field_name
        self.display_name = display_name
        self.default = default
        self.metric_type = metric_type

    def __str__(self):
        return "SRMetric: [%s, %s, %s, %s]" % (self.field_name, self.display_name, self.default, self.metric_type)


class Match(models.Model):

    matchNumber = models.IntegerField()

    def __str__(self):
        return "Match %s" % self.matchNumber


class Team(models.Model):

    teamNumber = models.IntegerField()

    def get_metrics(self):
        metrics = self.scoreresult_set.aggregate(Avg('TubesDropped'),
                                                 Avg('LowTubesHung'),
                                                 Avg('MidTubesHung'),
                                                 Avg('HighTubesHung'),
                                                 Avg('TubesRecieved'),
                                                 Avg('Penelties'),
                                                 Avg('MiniBotFinish'),
                                                 Avg('ScoredUberTube'),
                                                 Sum('DeployedMinibot'),
                                                 Sum('WasOffensive'),
                                                 Sum('WasScouted'),
                                                 Sum('BrokeBadly'),
                                                 Sum('Comments'),
                                                 )

        # Format all of the numbers.  If we haven't scouted the team, None will be returned.  Turn that into NA
        for key in metrics:
            if metrics[key] == None:
                metrics[key] = "NA"
            elif "__avg" in key:
                metrics[key] = "{:10.2f}".format(metrics[key])

        return metrics

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
    @staticmethod
    def get_fields():

        output = {}

        # Autonomous
        output['ScoredUberTube'] = ScoreResultMetric('ScoredUberTube', 'Scored Uber Tube', 0, "Average")

        # Tubes
        output['LowTubesHung'] = ScoreResultMetric('LowTubesHung', 'LowTubesHung', 0, "Average")
        output['MidTubesHung'] = ScoreResultMetric('MidTubesHung', 'MidTubesHung', 0, "Average")
        output['HighTubesHung'] = ScoreResultMetric('HighTubesHung', 'HighTubesHung', 0, "Average")
        output['TubesRecieved'] = ScoreResultMetric('TubesRecieved', 'TubesRecieved', 0, "Average")

        # Minibot
        output['MiniBotFinish'] = ScoreResultMetric('MiniBotFinish', 'MiniBotFinish')
        output['DeployedMinibot'] = ScoreResultMetric('DeployedMinibot', 'DeployedMinibot', 0, "Sum")

        # General
        output['Penelties'] = ScoreResultMetric('Penelties', 'Penelties', 0, "Average")
        output['WasOffensive'] = ScoreResultMetric('WasOffensive', 'WasOffensive', False, "Sum")
        output['WasScouted'] = ScoreResultMetric('WasScouted', 'WasScouted', False, "Sum")
        output['BrokeBadly'] = ScoreResultMetric('BrokeBadly', 'BrokeBadly', False, "Sum")
        output['Comments'] = ScoreResultMetric('Comments', 'Comments', "")

        return output
