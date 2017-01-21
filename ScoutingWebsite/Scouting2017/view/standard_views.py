from BaseScouting.views.base_views import BaseHomepageView, BaseAllTeamsViews,\
    BaseAllMatchesView, BaseSingleTeamView
from Scouting2017.model.reusable_models import Competition, TeamCompetesIn, Match, OfficialMatch, Team, TeamPictures, TeamComments
from Scouting2017.model.models2017 import get_team_metrics

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
    
class AllMatchesViews2017(BaseAllMatchesView):
    def __init__(self):
        BaseAllMatchesView.__init__(self, Match, OfficialMatch, 'Scouting2017/allmatches.html')

class SingleTeamView2017(BaseSingleTeamView):

    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, 'Scouting2017/view_team.html')

    def get_metrics(self, team):
        return []

