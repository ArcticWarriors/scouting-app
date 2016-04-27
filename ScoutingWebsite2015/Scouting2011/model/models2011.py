'''
Created on Apr 11, 2016

@author: PJ
'''
import collections
from django.db.models.aggregates import Avg, Sum
from django.db import models
from Scouting2011.model.reusable_models import ScoreResultMetric, Team, Match, Compitition


class ScoreResult(models.Model):

    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)
    competition = models.ForeignKey(Compitition)

    # auton
    scored_uber_tube = models.BooleanField()

    # Tubes
    low_tubes_hung = models.IntegerField()
    mid_tubes_hung = models.IntegerField()
    high_tubes_hung = models.IntegerField()
    tubes_dropped = models.IntegerField()
    tubes_received = models.IntegerField()

    # Minibot
    minibot_finish = models.IntegerField()
    deployed_minibot = models.BooleanField()

    # General
    penelties = models.IntegerField()
    was_offensive = models.BooleanField()
    was_scouted = models.BooleanField()
    broke_badly = models.BooleanField()
    comments = models.CharField(max_length=1000)

    @staticmethod
    def get_fields():

        output = collections.OrderedDict()

        # Autonomous
        output['scored_uber_tube'] = ScoreResultMetric('scored_uber_tube', 'Scored Uber Tube', 0, "Average")

        # Tubes
        output['low_tubes_hung'] = ScoreResultMetric('low_tubes_hung', 'LowTubesHung', 0, "Average")
        output['mid_tubes_hung'] = ScoreResultMetric('mid_tubes_hung', 'MidTubesHung', 0, "Average")
        output['high_tubes_hung'] = ScoreResultMetric('high_tubes_hung', 'HighTubesHung', 0, "Average")
        output['tubes_dropped'] = ScoreResultMetric('tubes_dropped', 'Tubes Dropped', 0, "Average")
        output['tubes_received'] = ScoreResultMetric('tubes_received', 'TubesRecieved', 0, "Average")

        # Minibot
        output['minibot_finish'] = ScoreResultMetric('minibot_finish', 'MiniBotFinish', 0)
        output['deployed_minibot'] = ScoreResultMetric('deployed_minibot', 'DeployedMinibot', 0, "Sum")

        # General
        output['penelties'] = ScoreResultMetric('penelties', 'Penelties', 0, "Average")
        output['was_offensive'] = ScoreResultMetric('was_offensive', 'WasOffensive', False, "Sum")
        output['was_scouted'] = ScoreResultMetric('was_scouted', 'WasScouted', False, "Sum")
        output['broke_badly'] = ScoreResultMetric('broke_badly', 'BrokeBadly', False, "Sum")
        output['comments'] = ScoreResultMetric('comments', 'Comments', "")

        return output


def get_team_metrics(team, all_fields=ScoreResult.get_fields()):

    kargs = {}
    field_order = []
    for key in all_fields:
        sr_field = all_fields[key]
        field_order.append(sr_field.display_name)
        if sr_field.metric_type == "Average":
            kargs[sr_field.display_name] = Avg(key)
        elif sr_field.metric_type == "Sum":
            kargs[sr_field.display_name] = Sum(key)
        else:
            print "field %s is not metrics-able" % key

    results = team.scoreresult_set.aggregate(**kargs)
    output = []
    for key in all_fields:
        sr_field = all_fields[key]
        if sr_field.display_name in results:
            output.append((sr_field.display_name, results[sr_field.display_name]))

    return output
