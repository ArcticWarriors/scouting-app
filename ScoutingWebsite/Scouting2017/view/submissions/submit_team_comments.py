
from Scouting2017.model.reusable_models import Team, TeamComments
from BaseScouting.views.submissions.submit_team_comments import BaseAddTeamCommentsView


class AddTeamCommentsView2017(BaseAddTeamCommentsView):

    def __init__(self):
        BaseAddTeamCommentsView.__init__(self, Team, TeamComments, 'Scouting2017:view_team')
