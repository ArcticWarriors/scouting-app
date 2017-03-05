from BaseScouting.views.base_views import BaseHomepageView
from Scouting2011.model import Competition, ScoreResult, Team
from django.db.models.aggregates import Avg
from Scouting2011.model.models2011 import get_team_metrics
from Scouting2011.model.reusable_models import Match, OfficialMatch


class HomepageView2011(BaseHomepageView):

    def __init__(self):
        BaseHomepageView.__init__(self, Competition, Team, Match, OfficialMatch, 'Scouting2011/index.html')

    def _get_our_team_number(self):
        return 229

    def _get_our_metrics(self, competition):

        team_search = Team.objects.filter(teamNumber=self._get_our_team_number())

        if len(team_search) == 0:
            return None

        all_fields = ScoreResult.get_fields()
        metrics_of_interest = {}
        metrics_of_interest['scored_uber_tube'] = all_fields['scored_uber_tube']
        metrics_of_interest['high_tubes_hung'] = all_fields['high_tubes_hung']
        metrics_of_interest['mid_tubes_hung'] = all_fields['mid_tubes_hung']
        metrics_of_interest['low_tubes_hung'] = all_fields['low_tubes_hung']

        return get_team_metrics(team_search[0], metrics_of_interest)

    def _get_competition_metrics(self, competition):

        num_to_display = 5

        metrics_names = []
        metrics_names.append(('scored_uber_tube', "Scored Uber Tube"))
        metrics_names.append(('high_tubes_hung', "High Tubes"))
        metrics_names.append(('mid_tubes_hung', "Mid Tubes"))
        metrics_names.append(('low_tubes_hung', "Low Tubes"))

        output = []

        for metric, full_name in metrics_names:
            result = ScoreResult.objects.filter(competition=competition).values('team__teamNumber').annotate(the_result=Avg(metric)).order_by('-the_result')[0:num_to_display]

            this_result = [(x['team__teamNumber'], "%.2f" % x['the_result']) for x in result]
            print this_result
            output.append((full_name, this_result))

        return output

    def _predict_match(self, match, competition):
        return None
