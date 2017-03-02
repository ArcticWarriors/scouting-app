from BaseScouting.views.base_views import BaseTeamListView
from Scouting2016.model.reusable_models import TeamCompetesIn
from Scouting2016.model.models2016 import ScoreResult, get_team_metrics


class TeamListView2016(BaseTeamListView):

    def __init__(self):
        BaseTeamListView.__init__(self, TeamCompetesIn, ScoreResult)

    def get_metrics_for_team(self, team):
        return get_team_metrics(team)
