from BaseScouting.views.base_views import BaseHomepageView
from Scouting2016.model.reusable_models import Team, Competition
from Scouting2016.model.models2016 import ScoreResult, get_advanced_team_metrics
from django.db.models.aggregates import Avg


class HomepageView2016(BaseHomepageView):

    def __init__(self):
        BaseHomepageView.__init__(self, Competition)

    def get_our_metrics(self):

        team_search = Team.objects.filter(teamNumber=174)

        if len(team_search) == 0:
            return None

        all_fields = ScoreResult.get_fields()
        metrics_of_interest = {}
        metrics_of_interest['low_score_successful'] = all_fields['low_score_successful']

        return get_advanced_team_metrics(team_search[0], metrics_of_interest)

    def get_competition_metrics(self, competition):

        num_to_display = 5

        metrics_names = []
        metrics_names.append(('high_score_successful', "High Goals"))
        metrics_names.append(('auto_score_high', "Auton High Goals"))
        metrics_names.append(('low_score_successful', "Low Goals"))
        metrics_names.append(('auto_score_low', "Auton Low Goals"))

        output = []

        for metric, full_name in metrics_names:
            result = ScoreResult.objects.filter(competition=competition).values('team__teamNumber').annotate(the_result=Avg(metric)).order_by('-the_result')[0:num_to_display]

            this_result = [(x['team__teamNumber'], "%.2f" % x['the_result']) for x in result]
            output.append((full_name, this_result))

        return output