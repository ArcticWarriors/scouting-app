from BaseScouting.views.standard_views.base_team_list import BaseTeamListView
from Scouting2017.model.reusable_models import TeamCompetesIn
from Scouting2017.model.models2017 import ScoreResult
from Scouting2017.model.get_stastics import get_statistics
from Scouting2017.model.get_team_metrics import get_team_metrics


class TeamListView2017(BaseTeamListView):
    def __init__(self):
        BaseTeamListView.__init__(self, TeamCompetesIn, ScoreResult, 'Scouting2017/team_list.html')

    def _get_metrics_for_team(self, team, regional_code):
        return get_team_metrics(team, regional_code)

    def get_context_data(self, **kwargs):

        user = self.request.user

        context = BaseTeamListView.get_context_data(self, **kwargs)
        reg_code = kwargs['regional_code']
#         teams_at_competition = TeamCompetesIn.objects.filter(competition__code=reg_code)
        stats = get_statistics(reg_code, context['teams'])
        context['stats'] = stats[0]
        context['skills'] = stats[1]

        for team in context['teams']:
            team.bookmarkCount = team.bookmarks.count()
            team.dnpCount = team.do_not_picks.count()

            if user != None and user.is_authenticated():
                team.isBookmarked = team in user.scout.bookmarked_teams.all()
                team.isDoNotPick = team in user.scout.do_not_pick_teams.all()
#             team.isBookmarked = user.scou

        return context
