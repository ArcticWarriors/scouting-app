from BaseScouting.views.base_views import BaseSingleTeamView
from Scouting2016.model.reusable_models import Team, TeamPictures, TeamComments
from Scouting2016.model.models2016 import get_team_metrics, TeamPitScouting


class SingleTeamView2016(BaseSingleTeamView):

    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, TeamPitScouting, 'BaseScouting/team.html')

    def get_metrics(self, team):
        return get_team_metrics(team)
