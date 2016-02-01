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


class OfficialMatch(models.Model):

    matchNumber = models.IntegerField()

    redTeam1 = models.IntegerField()
    redTeam2 = models.IntegerField()
    redTeam3 = models.IntegerField()
    blueTeam1 = models.IntegerField()
    blueTeam2 = models.IntegerField()
    blueTeam3 = models.IntegerField()

    redScore = models.IntegerField(default=-1)
    blueScore = models.IntegerField(default=-1)


class Team(models.Model):

    teamNumber = models.IntegerField()

    def get_metrics(self):
        metrics = self.scoreresult_set.aggregate(Avg('auton_score'),
                                                 Avg('pyramid_goals'),
                                                 Avg('high_goals'),
                                                 Avg('mid_goals'),
                                                 Avg('low_goals'),
                                                 Avg('missed_shots'),
                                                 Avg('hanging_points'),
                                                 Avg('fouls'),
                                                 Avg('technical_fouls'),
                                                 Sum('invalid_hangs'),
                                                 Sum('yellow_card'),
                                                 Sum('red_card'),
                                                 Sum('broke_badly'),
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

    @staticmethod
    def get_fields():

        output = {}

        output['auton_score'] = ScoreResultMetric('auton_score', 'Auton Score', 0, "Average")

        # Frisbees
        output['pyramid_goals'] = ScoreResultMetric('pyramid_goals', 'Pyramid', 0, "Average")
        output['high_goals'] = ScoreResultMetric('high_goals', 'High Goals', 0, "Average")
        output['mid_goals'] = ScoreResultMetric('mid_goals', 'Mid Goals', 0, "Average")
        output['low_goals'] = ScoreResultMetric('low_goals', 'Low Goals', 0, "Average")
        output['hanging_points'] = ScoreResultMetric('hanging_points', 'Hanging Points', 0, "Average")

        # General
        output['invalid_hangs'] = ScoreResultMetric('invalid_hangs', 'Invalid Hangs', "", "Sum")
        output['notes_text_area'] = ScoreResultMetric('notes_text_area', 'Notes', "")
        output['fouls'] = ScoreResultMetric('fouls', 'Tech Fouls', 0, "Fouls", "Sum")
        output['technical_fouls'] = ScoreResultMetric('technical_fouls', 'Tech Fouls', 0, "Sum")
        output['yellow_card'] = ScoreResultMetric('yellow_card', 'Yellow Card', 0, "Sum")
        output['red_card'] = ScoreResultMetric('red_card', 'Red Card', 0, "Sum")
        output['broke_badly'] = ScoreResultMetric('broke_badly', 'Broke Badly', 0, "Sum")

        return output
