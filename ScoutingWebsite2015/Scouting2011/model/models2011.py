'''
Created on Apr 11, 2016

@author: PJ
'''
from django.db.models.aggregates import Avg, Sum
from django.db import models
from Scouting2011.model.reusable_models import ScoreResultMetric, Team, \
    OfficialMatch, Match, Compitition



class ScoreResult(models.Model):

    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)
    competition = models.ForeignKey(Compitition)
    
    #auton
    scored_uber_tube    = models.BooleanField()
    
    #Tubes
    low_tubes_hung      = models.IntegerField()
    mid_tubes_hung      = models.IntegerField()
    high_tubes_hung     = models.IntegerField()
    tubes_dropped      = models.IntegerField()
    tubes_received     = models.IntegerField()
    
    #Minibot
    minibot_finish     = models.IntegerField()
    deployed_minibot   = models.BooleanField()
    
    #General
    penelties         = models.IntegerField()
    was_offensive      = models.BooleanField()
    was_scouted        = models.BooleanField()
    broke_badly        = models.BooleanField()
    comments          = models.CharField(max_length=1000)
    
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
