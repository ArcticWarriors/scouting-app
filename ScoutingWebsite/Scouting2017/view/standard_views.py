from BaseScouting.views.base_views import BaseHomepageView, BaseAllTeamsViews,\
    BaseAllMatchesView, BaseSingleTeamView
from Scouting2017.model.reusable_models import Competition, TeamCompetesIn, Match, OfficialMatch, Team, TeamPictures, TeamComments
from Scouting2017.model.models2017 import get_team_metrics, ScoreResult

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
            global_gear_sum .join(team.gears_score)
            teams_with_gears += 1
    
       
        
        global_gear_avg = 0 #some number
        
        for team in teams_at_competition:
            pass
        
            #compare global to me
            
        
            
    
class AllMatchesViews2017(BaseAllMatchesView):
    def __init__(self):
        BaseAllMatchesView.__init__(self, Match, OfficialMatch, 'Scouting2017/allmatches.html')

class SingleTeamView2017(BaseSingleTeamView):

    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, 'Scouting2017/view_team.html')

    def get_metrics(self, team):
        return []

