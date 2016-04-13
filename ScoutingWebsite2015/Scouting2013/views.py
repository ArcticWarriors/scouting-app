import operator

from django.core.urlresolvers import reverse_lazy

from Scouting2013.models import Team, Match, ScoreResult, TeamPictures, OfficialMatch, TeamComments
from Scouting2013.view.generic_views import SingleTeamView, SingleMatchView, \
    AllTeamsViews, AddTeamPictureView
from Scouting2013.model.models2013 import get_team_metrics


login_reverse = reverse_lazy('Scouting2013:showLogin')


class AllTeamsViews2013(AllTeamsViews):

    def get_metrics_for_team(self, team):
        return get_team_metrics(team)


class AddTeamPictureView2013(AddTeamPictureView):

    def __init__(self):
        AddTeamPictureView.__init__(self, 'Scouting2013/static', 'Scouting2013/robot_pics')


class SingleTeamView2013(SingleTeamView):

    def get_metrics(self, team):
        return get_team_metrics(team)


class SingleMatchView2013(SingleMatchView):
    
    def get_metrics(self, sr):
        output = []
        output.append(('teamNumber', sr.team.teamNumber))
        sr_fields = ScoreResult.get_fields()
        for key in sr_fields:
            sr_field = sr_fields[key]
            output.append((sr_field.display_name, getattr(sr, key)))
            
        return output

