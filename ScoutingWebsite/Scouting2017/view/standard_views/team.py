from BaseScouting.views.standard_views.base_team import BaseSingleTeamView
from Scouting2017.model.reusable_models import Team, TeamPictures, TeamComments
from Scouting2017.model.models2017 import TeamPitScouting
from Scouting2017.model.get_team_metrics import get_team_metrics


class SingleTeamView2017(BaseSingleTeamView):

    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, TeamPitScouting, 'Scouting2017/team.html')

    def get_metrics(self, team):
        return get_team_metrics(team)
