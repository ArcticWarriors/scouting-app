'''
Created on Jan 29, 2016

@author: PJ
'''

from Scouting2016.models import *
from Scouting2016.views import *
import random
import numbers
    
    
def __get_score_result_fields():
    
    output = {}
    
    output['auto_score_high'] = 0
    output['auto_score_low'] = 0
    output['cheval_de_frise'] = 0
    output['draw_bridge'] = 0
    output['high_score_fail'] = 0
    output['high_score_successful'] = 0
    output['low_bar'] = 0
    output['low_score_fail'] = 0
    output['low_score_successful'] = 0
    output['moat'] = 0
    output['notes_text_area'] = 0
    output['ramparts'] = 0
    output['rock_wall'] = 0
    output['rough_terrain'] = 0
    output['score_tech_foul'] = 0
    output['sally_port'] = 0
    output['portcullis'] = 0
    output['auto_spy'] = 'yes'
    output['auto_defense'] = 'no_reach'
    output['scale_challenge'] = 'partial'    
    output['slow_fast_bridge'] = 'slow'
    output['slow_fast_cheval'] = 'fast'
    output['slow_fast_low_bar'] = 'slow'
    output['slow_fast_moat'] = 'slow'
    output['slow_fast_portcullis'] = 'slow'
    output['slow_fast_ramparts'] = 'no_move'
    output['slow_fast_rock_wall'] = 'no_move'
    output['slow_fast_rough'] = 'slow'
    output['slow_fast_sally'] = 'slow'
    
    return output
    
    
def __get_create_kargs():
    
    kargs = {}
    
    score_result_fields_with_default= __get_score_result_fields()
    
    for field_name in score_result_fields_with_default:
        
        if isinstance(score_result_fields_with_default[field_name], numbers.Number):
            kargs[field_name] = random.randint(0, 6)
        else:
            kargs[field_name] = score_result_fields_with_default[field_name]
            
            
    return kargs
        
          

def create_teams():
    
    Team.objects.create(teamNumber=73)
    Team.objects.create(teamNumber=120)
    Team.objects.create(teamNumber=145)
    Team.objects.create(teamNumber=174)
    Team.objects.create(teamNumber=191)
    Team.objects.create(teamNumber=229)
    Team.objects.create(teamNumber=250)
    Team.objects.create(teamNumber=340)
    Team.objects.create(teamNumber=378)
    Team.objects.create(teamNumber=578)
    Team.objects.create(teamNumber=639)
    Team.objects.create(teamNumber=1126)
    Team.objects.create(teamNumber=1405)
    Team.objects.create(teamNumber=1450)
    Team.objects.create(teamNumber=1507)
    Team.objects.create(teamNumber=1511)
    Team.objects.create(teamNumber=1518)
    Team.objects.create(teamNumber=1551)
    Team.objects.create(teamNumber=1559)
    Team.objects.create(teamNumber=1591)
    Team.objects.create(teamNumber=1765)
    Team.objects.create(teamNumber=2053)
    Team.objects.create(teamNumber=2172)
    Team.objects.create(teamNumber=2228)
    Team.objects.create(teamNumber=2340)
    Team.objects.create(teamNumber=3003)
    Team.objects.create(teamNumber=3015)
    Team.objects.create(teamNumber=3044)
    Team.objects.create(teamNumber=3157)
    Team.objects.create(teamNumber=3181)
    Team.objects.create(teamNumber=3613)
    Team.objects.create(teamNumber=3687)
    Team.objects.create(teamNumber=3799)
    Team.objects.create(teamNumber=3838)
    Team.objects.create(teamNumber=3842)
    Team.objects.create(teamNumber=3951)
    Team.objects.create(teamNumber=4093)
    Team.objects.create(teamNumber=4124)
    Team.objects.create(teamNumber=4203)
    Team.objects.create(teamNumber=843)
    Team.objects.create(teamNumber=3173)

def create_matches():
    
    Match.objects.create(matchNumber=1)
    Match.objects.create(matchNumber=2)
    Match.objects.create(matchNumber=3)
    Match.objects.create(matchNumber=4)
    Match.objects.create(matchNumber=5)
    Match.objects.create(matchNumber=7)
    Match.objects.create(matchNumber=8)
    Match.objects.create(matchNumber=9)
    Match.objects.create(matchNumber=10)
    Match.objects.create(matchNumber=11)
    Match.objects.create(matchNumber=12)
    Match.objects.create(matchNumber=13)
    Match.objects.create(matchNumber=14)
    Match.objects.create(matchNumber=15)
    Match.objects.create(matchNumber=16)
    Match.objects.create(matchNumber=17)
    Match.objects.create(matchNumber=18)
    Match.objects.create(matchNumber=19)
    Match.objects.create(matchNumber=20)
    Match.objects.create(matchNumber=22)
    Match.objects.create(matchNumber=23)
    Match.objects.create(matchNumber=24)
    Match.objects.create(matchNumber=25)
    Match.objects.create(matchNumber=26)
    Match.objects.create(matchNumber=27)
    Match.objects.create(matchNumber=28)
    Match.objects.create(matchNumber=29)
    Match.objects.create(matchNumber=30)
    Match.objects.create(matchNumber=31)
    Match.objects.create(matchNumber=32)
    Match.objects.create(matchNumber=33)
    Match.objects.create(matchNumber=34)
    Match.objects.create(matchNumber=35)
    Match.objects.create(matchNumber=36)
    Match.objects.create(matchNumber=37)
    Match.objects.create(matchNumber=38)
    Match.objects.create(matchNumber=39)
    Match.objects.create(matchNumber=40)
    
    
def create_scoreresults():
    
    teams = Team.objects.all()
    matches = Match.objects.all()
    
    for match in matches:
        team_indices = []
        
        while len(team_indices) < 6:
            team_index = random.randint(0, len(teams) - 1)
            if team_index not in team_indices:
                team_indices.append(team_index)
                
        for i in team_indices:
            team = teams[i]
            
            kargs = __get_create_kargs()
            ScoreResult.objects.create(match=match,  team=team, **kargs)
        