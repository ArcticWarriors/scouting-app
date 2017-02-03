from BaseScouting.views.base_views import BaseHomepageView, BaseTeamListView,\
    BaseSingleMatchView, BaseMatchListView, BaseSingleTeamView, BaseMatchEntryView
from Scouting2017.model.reusable_models import Competition, TeamCompetesIn, Match, OfficialMatch, Team, TeamPictures, TeamComments
from Scouting2017.model.models2017 import get_team_metrics, ScoreResult
from django.db.models.aggregates import Avg, Sum
from django.db.models.expressions import Case, When
import math

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
        
        get_statistics(reg_code, context['teams']) 
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
When get_statistics() function is called, it grabs live data from all the teams and all their score results.
It then will use that data to determine a mean and standard deviation for bots' gears,fuel,and rope capabilities.
get_statistics() will also calculate z-scores along the St. Dev. for those elements and store them in the model to be called later.
'''
def get_statistics(regional_code, teams_at_competition):
    competition_srs = ScoreResult.objects.filter(competition__code=regional_code)
    competition_averages = competition_srs.aggregate(Avg('gears_score'),
                                                    Avg('fuel_score_hi'),
                                                    Avg('fuel_score_hi_auto'),
                                                    Avg('fuel_score_low'),
                                                    Avg('fuel_score_low_auto'),
                                                    rope__avg = Avg(Case(When(rope=True, then=1),When(rope=False, then=0))))
    num_srs = 0 
    rope_avg = competition_averages['rope__avg']
    print rope_avg
    gear_avg = competition_averages['gears_score__avg']
    fuel_avg = competition_averages['fuel_score_hi_auto__avg'] + (competition_averages['fuel_score_hi__avg'] / 3 ) + (competition_averages['fuel_score_low_auto__avg'] / 3) + (competition_averages['fuel_score_low__avg'] / 9)
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
    print rope_stdev
    
    for team in teams_at_competition:
        teams_srs = team.scoreresult_set.filter(competition__code=regional_code) 
        team_avgs = teams_srs.aggregate(Avg('gears_score'),
                                        Avg('fuel_score_hi'),
                                        Avg('fuel_score_hi_auto'),
                                        Avg('fuel_score_low'),
                                        Avg('fuel_score_low_auto'),
                                        team_rope__avg = Avg(Case(When(rope=True, then=1),When(rope=False, then=0))))
                                      
        team_rope_avg = team_avgs['team_rope__avg']
        print team_rope_avg
        team.fuel_z = 'NA'
        team.gear_z = 'NA'
        team.rope_z = 'NA'
        team.rope_pct = 'NA'
        if len(teams_srs)!= 0:
            team.gear_z = (team_avgs['gears_score__avg'] - gear_avg ) / gear_stdev 
            team.fuel_z = (((team_avgs['fuel_score_hi_auto__avg']) + (team_avgs['fuel_score_hi__avg'] / 3) + (team_avgs['fuel_score_low_auto__avg'] / 3) + (team_avgs['fuel_score_low__avg']/ 9)) - fuel_avg) / fuel_stdev
            team.rope_z = (team_avgs['team_rope__avg'] - rope_avg) / rope_stdev
            team.rope_pct = team_avgs['team_rope__avg'] * 100