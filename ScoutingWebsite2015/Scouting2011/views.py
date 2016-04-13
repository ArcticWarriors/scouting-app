import operator

from django.core.urlresolvers import reverse_lazy

from Scouting2011.models import Team, Match, ScoreResult, TeamPictures, OfficialMatch, TeamComments
from Scouting2011.view.generic_views import SingleTeamView, SingleMatchView, \
    AllTeamsViews, AddTeamPictureView
from Scouting2011.model.models2011 import get_team_metrics


login_reverse = reverse_lazy('Scouting2011:showLogin')


class AllTeamsViews2011(AllTeamsViews):

    def get_metrics_for_team(self, team):
        all_fields=ScoreResult.get_fields()
        
        return get_team_metrics(team, all_fields)


class AddTeamPictureView2011(AddTeamPictureView):

    def __init__(self):
        AddTeamPictureView.__init__(self, 'Scouting2011/static', 'Scouting2011/robot_pics')


class SingleTeamView2011(SingleTeamView):

    def get_metrics(self, team):
        all_fields=ScoreResult.get_fields()
        del all_fields['was_offensive']
        
        return get_team_metrics(team, all_fields)


class SingleMatchView2011(SingleMatchView):
    
    def get_metrics(self, sr):
        output = []
        output.append(('teamNumber', sr.team.teamNumber))
        sr_fields = ScoreResult.get_fields()
        for key in sr_fields:
            sr_field = sr_fields[key]
            output.append((sr_field.display_name, getattr(sr, key)))
            
        return output

