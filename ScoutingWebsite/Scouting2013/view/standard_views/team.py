from BaseScouting.views.base_views import BaseSingleTeamView
from Scouting2013.model.reusable_models import Team, TeamPictures, TeamComments
from Scouting2013.model.models2013 import get_team_metrics


class SingleTeamView2013(BaseSingleTeamView):

    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, 'Scouting2013/view_team.html')

    def get_metrics(self, team):
        return get_team_metrics(team)