import operator

from django.core.urlresolvers import reverse_lazy

from Scouting2013.models import Team, Match, ScoreResult, TeamPictures, OfficialMatch, TeamComments
from Scouting2013.view.generic_views import SingleTeamView, SingleMatchView, \
    AllTeamsViews, AddTeamPictureView
from Scouting2013.model.models2013 import get_team_metrics


login_reverse = reverse_lazy('Scouting2013:showLogin')


class AllTeamsViews2013(AllTeamsViews):

    def get_metrics_for_team(self, team):
        xxx = get_team_metrics(team)
        print "AHHHHHHHHHHHHHHHHHH"
        print xxx
        return xxx


class AddTeamPictureView2013(AddTeamPictureView):

    def __init__(self):
        AddTeamPictureView.__init__(self, 'Scouting2013/static', 'Scouting2013/robot_pics')


class SingleTeamView2013(SingleTeamView):

    def get_metrics(self, team):
        xxx = get_team_metrics(team)
        print "AHHHHHHHHHHHHHHHHHH"
        print xxx
        return xxx


class SingleMatchView2013(SingleMatchView):
    pass

