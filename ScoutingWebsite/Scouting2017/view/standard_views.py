from BaseScouting.views.base_views import BaseHomepageView, BaseTeamListView,\
    BaseSingleMatchView, BaseMatchListView, BaseSingleTeamView, BaseMatchEntryView
from Scouting2017.model.reusable_models import Competition, TeamCompetesIn, Match, OfficialMatch, Team, TeamPictures, TeamComments
from Scouting2017.model.models2017 import get_team_metrics, ScoreResult
from django.db.models.aggregates import Avg, Sum
from django.db.models.expressions import Case, When
import math,json

class HomepageView2017(BaseHomepageView):
 
    def __init__(self):
        BaseHomepageView.__init__(self, Competition, 'BaseScouting/index.html')
 
    def get_our_metrics(self):
 
        return []
 
    def get_competition_metrics(self, competition):
 
        output = []
 
        return output

class TeamListView2017(BaseTeamListView):
    def __init__(self):
        BaseTeamListView.__init__(self, TeamCompetesIn, ScoreResult, 'Scouting2017/team_list.html')

    def get_metrics_for_team(self, team):
        return get_team_metrics(team)
    
    def get_context_data(self, **kwargs):
        context = BaseTeamListView.get_context_data(self, **kwargs)
        reg_code = kwargs['regional_code']
#         teams_at_competition = TeamCompetesIn.objects.filter(competition__code=reg_code)
        stats = get_statistics(reg_code, context['teams'])
        context['stats'] = stats[0]
        context['skills'] = stats[1]
        return context
        
class SingleMatchView2017(BaseSingleMatchView):

    def __init__(self):
        BaseSingleMatchView.__init__(self, Match, 'Scouting2017/match.html')

    def get_metrics(self, score_result):
        return []

class MatchListView2017(BaseMatchListView):
    def __init__(self):
        BaseMatchListView.__init__(self, Match, OfficialMatch)

class SingleTeamView2017(BaseSingleTeamView):

    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, 'Scouting2017/team.html')

    def get_metrics(self, team):
        return get_team_metrics(team)

class MatchEntryView2017(BaseMatchEntryView):
    def __init__(self):
        BaseMatchEntryView.__init__(self, 'Scouting2017/match_entry.html')

    
'''
The get_statistics function() returns two lists of metrics.
The first thing it returns, stats, is a dictionary containing the values of overall averages for all score results, along with standard deviations for those same score results along the mean.
The function also returns a list called skills, which contains data for each team including their z-scores, calculated fuel scores for both hi, low, autonomous, teleop, and overall, and their accuracy in climbing the rope. 
'''
def get_statistics(regional_code, teams_at_competition):
    
    skills = []
       
    competition_srs = ScoreResult.objects.filter(competition__code=regional_code)
    competition_averages = competition_srs.aggregate(Avg('gears_score'),
                                                    Avg('fuel_score_hi'),
                                                    Avg('fuel_score_hi_auto'),
                                                    Avg('fuel_score_low'),
                                                    Avg('fuel_score_low_auto'),
                                                    rope__avg = Avg(Case(When(rope=True, then=1),When(rope=False, then=0))))
    rope_avg = competition_averages['rope__avg']
    gear_avg = competition_averages['gears_score__avg']
    fuel_avg = competition_averages['fuel_score_hi_auto__avg'] + (competition_averages['fuel_score_hi__avg'] / 3 ) + (competition_averages['fuel_score_low_auto__avg'] / 3) + (competition_averages['fuel_score_low__avg'] / 9)
   # This part of the function (above) obtains overall averages for all score results
    num_srs = 0 
    gear_v2 = 0
    fuel_v2 = 0
    rope_v2 = 0
    num_srs = 0 
    
    for sr in competition_srs: 
        if sr.rope==True:
            sr_rope =1-rope_avg
        else:
            sr_rope = 0-rope_avg     
        sr_gear = sr.gears_score - gear_avg
        sr_fuel = ((sr.fuel_score_hi_auto)+(sr.fuel_score_hi / 3) + (sr.fuel_score_low_auto / 3) + (sr.fuel_score_low / 9)) - fuel_avg
        gear_v2 += sr_gear * sr_gear
        fuel_v2 += sr_fuel * sr_fuel
        rope_v2 += sr_rope * sr_rope 
        num_srs += 1  
    gear_stdev = math.sqrt(gear_v2/num_srs) 
    fuel_stdev = math.sqrt(fuel_v2/num_srs)
    rope_stdev = math.sqrt(rope_v2/num_srs)
    # This part of the function (above) obtains overall standard deviations for all score results
    for team in teams_at_competition:
        teams_srs = team.scoreresult_set.filter(competition__code=regional_code) 
        team_avgs = teams_srs.aggregate(Avg('gears_score'),
                                        Avg('fuel_score_hi'),
                                        Avg('fuel_score_hi_auto'),
                                        Avg('fuel_score_low'),
                                        Avg('fuel_score_low_auto'),
                                        team_rope__avg = Avg(Case(When(rope=True, then=1),When(rope=False, then=0))))
                                      
        team_rope_avg = team_avgs['team_rope__avg']
        team.skills = {}
        team.skills['fuel_z'] = 'NA'
        team.skills['gear_z'] = 'NA'
        team.skills['rope_z'] = 'NA'
        team.skills['rope_pct'] = 'NA'
        if len(teams_srs)!= 0:
            team.skills['fuel_score'] = ((team_avgs['fuel_score_hi_auto__avg']) + (team_avgs['fuel_score_hi__avg'] / 3) + (team_avgs['fuel_score_low_auto__avg'] / 3) + (team_avgs['fuel_score_low__avg']/ 9))
            team.skills['gear_z'] = (team_avgs['gears_score__avg'] - gear_avg ) / gear_stdev 
            team.skills['fuel_z'] = (((team_avgs['fuel_score_hi_auto__avg']) + (team_avgs['fuel_score_hi__avg'] / 3) + (team_avgs['fuel_score_low_auto__avg'] / 3) + (team_avgs['fuel_score_low__avg']/ 9)) - fuel_avg) / fuel_stdev
            team.skills['rope_z'] = (team_avgs['team_rope__avg'] - rope_avg) / rope_stdev
            team.skills['rope_pct'] = team_avgs['team_rope__avg'] * 100
        skills.append({'team': team.teamNumber, 'skills':team.skills})
    
    stats = {'gear_avg': gear_avg, 'rope_avg': rope_avg, 'fuel_avg': fuel_avg, 'fuel_hi_avg': team_avgs['fuel_score_hi__avg'], 'fuel_low_avg': team_avgs['fuel_score_low__avg'],
             'fuel_hi_auto_avg': team_avgs['fuel_score_hi_auto__avg'], 'fuel_low_auto_avg': team_avgs['fuel_score_low_auto__avg'], 'gear_stdev': gear_stdev, 'rope_stdev': rope_stdev, 'fuel_stdev': fuel_stdev}
    #This part of the function creates the lists that are passed back.
    return (stats,json.dumps(skills))   