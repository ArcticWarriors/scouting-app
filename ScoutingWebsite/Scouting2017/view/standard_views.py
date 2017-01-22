from BaseScouting.views.base_views import BaseHomepageView, BaseAllTeamsViews,\
    BaseAllMatchesView, BaseSingleTeamView
from Scouting2017.model.reusable_models import Competition, TeamCompetesIn, Match, OfficialMatch, Team, TeamPictures, TeamComments
from Scouting2017.model.models2017 import get_team_metrics, ScoreResult
import math

class HomepageView2017(BaseHomepageView):
 
    def __init__(self):
        BaseHomepageView.__init__(self, Competition, 'Scouting2017/index.html')
 
    def get_our_metrics(self):
 
        return []
 
    def get_competition_metrics(self, competition):
 
        output = []
 
        return output

class AllTeamsViews2017(BaseAllTeamsViews):
    def __init__(self):
        BaseAllTeamsViews.__init__(self, TeamCompetesIn, 'Scouting2017/all_teams.html')

    def get_metrics_for_team(self, team):
        return get_team_metrics(team)
    
    def get_context_data(self, **kwargs):
        context = BaseAllTeamsViews.get_context_data(self, **kwargs)
        context['statistics'] = self.get_statistics(kwargs['regional_code'])
        

class AllMatchesViews2017(BaseAllMatchesView):
    def __init__(self):
        BaseAllMatchesView.__init__(self, Match, OfficialMatch, 'Scouting2017/allmatches.html')

class SingleTeamView2017(BaseSingleTeamView):

    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, 'Scouting2017/view_team.html')

    def get_metrics(self, team):
        return []

'''
When get_statistics() function is called, it grabs live data from all the teams and all their score results.
It then will use that data to determine a mean and SAMPLE standard deviation for bots' gears,fuel,and rope capabilities.
get_statistics() will also calculate z-scores along the SSD for those elements and store them in the model to be called later.
NOTE: Sample standard deviation is used when you do not have the full data set, so I believe it is appropriate to use here.
'''
def get_statistics(self, regional_code):
    competition_srs = ScoreResult.objects.filter(competition__code=regional_code)
    teams_at_competition = TeamCompetesIn.objects.filter(competition__code=regional_code)
    metrics = get_team_metrics(teams_at_competition)
    # black magic grabs all the metrics for every team with metrics.
        
    global_gear_sum = 0 # summation used to find global_gear_avg
    teams_with_gears = 0 #counter variable
        
    for team in metrics:
        global_gear_sum.join(team.gears_score__avg)
        teams_with_gears += 1
     
    if teams_with_gears==0: # Divide by 0 should not happen.
        global_gear_avg = 'NA'
    else:
        global_gear_avg = global_gear_sum/(teams_with_gears) # X-bar (Mean) for gears.
        # the above for loop will grab all the team's score results, and average them all together.
    print global_gear_avg
        
        
    teams_with_gears = 0 # Reset counter variable
    sum_v_squared = 0
    for team in teams_at_competition: # Finds the standard deviation
        sum_v_squared.join((team.gears_score__avg - global_gear_avg)**2) #Obtains a variance, squares it, and ads it to a sum.
        teams_with_gears += 1
            
    if teams_with_gears==1: # Divide by 0 should not happen. Is == 1 because SSD requires dividing by N-1, so having exactly 1 score result would break this.
        st_dev_gear = 'NA'
    else:          
        st_dev_gear = math.sqrt(sum_v_squared / (teams_with_gears-1)) # Standard deviation for gears.  
    print st_dev_gear
        
            
    gear_stat_z = 0    
    for team in teams_at_competition: # Finds Z-scores and ads them to each team's model.
        variance = (team.gears_score__avg - global_gear_avg)
        #gear_stat_z = variance/st_dev_gear 
        # this is commented until we figure out how to add it to the model
        
            