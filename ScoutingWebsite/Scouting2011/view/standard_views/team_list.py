from BaseScouting.views.base_views import BaseTeamListView
from Scouting2011.model.reusable_models import TeamCompetesIn
from Scouting2011.model.models2011 import ScoreResult, get_team_metrics


class AllTeamsViews2011(BaseTeamListView):

    def __init__(self):
        BaseTeamListView.__init__(self, TeamCompetesIn, ScoreResult, 'Scouting2011/all_teams.html')

    def get_metrics_for_team(self, team):
        all_fields = ScoreResult.get_fields()
        del all_fields['was_offensive']
        del all_fields['was_scouted']
        del all_fields['broke_badly']

        return get_team_metrics(team, all_fields)