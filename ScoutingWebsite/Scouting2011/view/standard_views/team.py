from BaseScouting.views.base_views import BaseSingleTeamView
from Scouting2011.model.reusable_models import Team, TeamPictures, TeamComments
from Scouting2011.model.models2011 import ScoreResult, get_team_metrics,\
    TeamPitScouting

class SingleTeamView2011(BaseSingleTeamView):

#     def __init__(self, team_model, team_pictures_model, team_comments_model, team_pit_scouting_model, template_name):
    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, TeamPitScouting, 'Scouting2011/view_team.html')

    def get_metrics(self, team):
        all_fields = ScoreResult.get_fields()
        del all_fields['was_offensive']

        return get_team_metrics(team, all_fields)