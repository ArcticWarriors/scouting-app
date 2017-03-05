from BaseScouting.views.base_views import BaseAddTeamCommentsView
from Scouting2016.model.reusable_models import Team, TeamComments


class AddTeamCommentsView2016(BaseAddTeamCommentsView):

    def __init__(self):
        BaseAddTeamCommentsView.__init__(self, Team, TeamComments, 'Scouting2016:view_team')
