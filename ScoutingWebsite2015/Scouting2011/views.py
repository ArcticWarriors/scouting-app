import operator

from django.core.urlresolvers import reverse_lazy

from Scouting2011.models import Team, Match, ScoreResult, TeamPictures, OfficialMatch, TeamComments
from Scouting2011.view.generic_views import SingleTeamView, SingleMatchView, \
    AllTeamsViews, AddTeamPictureView


login_reverse = reverse_lazy('Scouting2011:showLogin')


class AllTeamsViews2011(AllTeamsViews):

    def get_metrics_for_team(self, team):
        return []


class AddTeamPictureView2011(AddTeamPictureView):

    def __init__(self):
        AddTeamPictureView.__init__(self, 'Scouting2011/static', 'Scouting2011/robot_pics')


class SingleTeamView2011(SingleTeamView):

    def get_metrics(self, team):
        return []


class SingleMatchView2011(SingleMatchView):
    pass

