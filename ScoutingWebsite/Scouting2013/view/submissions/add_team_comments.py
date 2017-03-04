from BaseScouting.views.base_views import BaseAddTeamCommentsView
from Scouting2013.model.reusable_models import Team, TeamComments


class AddTeamCommentsView2013(BaseAddTeamCommentsView):

    def __init__(self):
        BaseAddTeamCommentsView.__init__(self, Team, TeamComments, 'Scouting2013:view_team')