from BaseScouting.views.base_views import BaseHomepageView
from Scouting2013.model.reusable_models import Competition
from Scouting2013.model.models2013 import ScoreResult
from django.db.models.aggregates import Avg

class HomepageView2013(BaseHomepageView):

    def __init__(self):
        BaseHomepageView.__init__(self, Competition, 'Scouting2013/index.html')

    def get_our_metrics(self):
        return None

    def get_competition_metrics(self, competition):

        num_to_display = 5

        metrics_names = []
        metrics_names.append(('hanging_points', "Hanging Points"))
        metrics_names.append(('pyramid_goals', "Pyramid Goals"))
        metrics_names.append(('high_goals', "High Goals"))
        metrics_names.append(('mid_goals', "Mid Goals"))
        metrics_names.append(('low_goals', "Low Goals"))

        output = []

        for metric, full_name in metrics_names:
            result = ScoreResult.objects.filter(competition=competition).values('team__teamNumber').annotate(the_result=Avg(metric)).order_by('-the_result')[0:num_to_display]

            this_result = [(x['team__teamNumber'], "%.2f" % x['the_result']) for x in result]
            print this_result
            output.append((full_name, this_result))

        return output