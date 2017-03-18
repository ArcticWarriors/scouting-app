'''
Created on Feb 22, 2017

@author: PJ
'''
from BaseScouting.views.base_views import BaseMatchEntryView
from Scouting2017.model.reusable_models import Match, TeamCompetesIn,\
    Competition
import collections
from Scouting2017.model.models2017 import ScoreResult
import json


class MatchEntryView2017(BaseMatchEntryView):
    def __init__(self):
        BaseMatchEntryView.__init__(self, 'Scouting2017/match_entry.html')
        
    def has_scouted_info(self, team, match):
        
        return len(ScoreResult.objects.filter(team=team, match=match)) == 1
        
    def get_context_data(self, **kwargs):
        context = super(BaseMatchEntryView, self).get_context_data(**kwargs)
        
        competition = Competition.objects.get(code=kwargs['regional_code'])
        matches = Match.objects.filter(competition=competition)
        
        matches_context = {}
        
        team_pair = TeamCompetesIn.objects.filter(competition=competition)
        context["teams"] = {pair.team.teamNumber: 0 for pair in team_pair }
        
        for match in matches:
            scouted = []
            unscouted = []
            
            if self.has_scouted_info(match.red1, match):
                scouted.append(match.red1.teamNumber)
            else:
                unscouted.append(match.red1.teamNumber)
                
            if self.has_scouted_info(match.red2, match):
                scouted.append(match.red2.teamNumber)
            else:
                unscouted.append(match.red2.teamNumber)
                
            if self.has_scouted_info(match.red3, match):
                scouted.append(match.red3.teamNumber)
            else:
                unscouted.append(match.red3.teamNumber)
            
            if self.has_scouted_info(match.blue1, match):
                scouted.append(match.blue1.teamNumber)
            else:
                unscouted.append(match.blue1.teamNumber)
                
            if self.has_scouted_info(match.blue2, match):
                scouted.append(match.blue2.teamNumber)
            else:
                unscouted.append(match.blue2.teamNumber)
                
            if self.has_scouted_info(match.blue3, match):
                scouted.append(match.blue3.teamNumber)
            else:
                unscouted.append(match.blue3.teamNumber)
            
            matches_context[match.matchNumber] = unscouted
        
        context["matches"] = matches_context

        return context
