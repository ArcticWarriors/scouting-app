'''
Created on Apr 11, 2016

@author: PJ
'''
from django.db.models.aggregates import Avg, Sum
from django.db import models
from Scouting2013.model.reusable_models import ScoreResultMetric, Team, \
    OfficialMatch, Match, Compitition



class ScoreResult(models.Model):

    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)
    competition = models.ForeignKey(Compitition)

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
        output['fouls'] = ScoreResultMetric('fouls', 'Fouls', 0, "Sum")
        output['technical_fouls'] = ScoreResultMetric('technical_fouls', 'Tech Fouls', 0, "Sum")
        output['yellow_card'] = ScoreResultMetric('yellow_card', 'Yellow Card', 0, "Sum")
        output['red_card'] = ScoreResultMetric('red_card', 'Red Card', 0, "Sum")
        output['broke_badly'] = ScoreResultMetric('broke_badly', 'Broke Badly', 0, "Sum")

        return output



def get_team_metrics(team):
    
    kargs = {}
    all_fields = ScoreResult.get_fields()
    for key in all_fields:
        sr_field = all_fields[key]
        if sr_field.metric_type == "Average":
#             kargs.append(Avg(key))
            kargs[sr_field.display_name] = Avg(key)
        elif sr_field.metric_type == "Sum":
#             kargs.append(Sum(key))
            kargs[sr_field.display_name] = Sum(key)
        else:
            print "field %s is not metrics-able" % key
            
    print kargs
    output =  team.scoreresult_set.aggregate(**kargs)
    print
    print
    print output
    print 
    print
    
    return output