from BaseScouting.views.base_views import BaseAddTeamCommentsView
from Scouting2011.model.reusable_models import Team, TeamComments


class AddTeamCommentsView2011(BaseAddTeamCommentsView):

    def __init__(self):
        BaseAddTeamCommentsView.__init__(self, Team, TeamComments, 'Scouting2011:view_team')