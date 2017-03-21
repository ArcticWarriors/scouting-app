from BaseScouting.views.standard_views.base_team import BaseSingleTeamView
from Scouting2017.model.reusable_models import Team, TeamPictures, TeamComments, \
    TeamCompetesIn
from Scouting2017.model.models2017 import TeamPitScouting
from Scouting2017.model.get_team_metrics import get_team_metrics


class SingleTeamView2017(BaseSingleTeamView):

    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, TeamPitScouting, TeamCompetesIn, 'Scouting2017/team.html')

    def _get_metrics(self, team, regional_code):
        return get_team_metrics(team, regional_code)
