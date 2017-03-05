from BaseScouting.views.base_views import BaseTeamListView
from Scouting2013.model.reusable_models import TeamCompetesIn
from Scouting2013.model.models2013 import get_team_metrics


class AllTeamsViews2013(BaseTeamListView):

    def __init__(self):
        BaseTeamListView.__init__(self, TeamCompetesIn, 'Scouting2013/all_teams.html')

    def get_metrics_for_team(self, team):
        return get_team_metrics(team)