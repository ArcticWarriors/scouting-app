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
        
    
    def get_statistics(self, regional_code):

        competition_srs = ScoreResult.objects.filter(competition__code=regional_code)
        teams_at_competition = TeamCompetesIn.objects.filter(competition__code=regional_code)
        metrics = get_team_metrics(teams_at_competition)
        # Average All the stuff
        global_gear_sum = 0
        teams_with_gears = 0
        
        for team in metrics:
            global_gear_sum.join(team.gears_score__avg)
            teams_with_gears += 1
    
       
        if teams_with_gears==0:
            global_gear_avg = 'NA'
        else:
            global_gear_avg = global_gear_sum/(teams_with_gears)
        print global_gear_avg #some number
        teams_with_gears = 0
        variance = 0
        sum_v_squared = 0
        for team in teams_at_competition:
            variance = (team.gears_score__avg - global_gear_avg)
            sum_v_squared.join(variance**2)
            teams_with_gears += 1
            #compare global to me
            gear_stat_z = 0
        if teams_with_gears==1:
            st_dev_gear = 'NA'
        else:          
            st_dev_gear = math.sqrt(sum_v_squared / (teams_with_gears-1))   
        for team in teams_at_competition:
            variance = (team.gears_score__avg - global_gear_avg)
            #gear_stat_z = variance/st_dev_gear 
            # this is commented until we figure out how to add it to the model
        
            
            
        
            
    
class AllMatchesViews2017(BaseAllMatchesView):
    def __init__(self):
        BaseAllMatchesView.__init__(self, Match, OfficialMatch, 'Scouting2017/allmatches.html')

class SingleTeamView2017(BaseSingleTeamView):

    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, 'Scouting2017/view_team.html')

    def get_metrics(self, team):
        return []

