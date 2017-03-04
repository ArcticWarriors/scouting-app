from BaseScouting.views.base_views import BaseMatchPredictionView
from Scouting2011.model.reusable_models import OfficialMatch


class OfficialMatchView2011(BaseMatchPredictionView):

    def __init__(self):
        BaseMatchPredictionView.__init__(self, OfficialMatch, 'Scouting2011/view_official_match.html')

    def get_score_results(self, official_match):

        results = official_match.officialmatchscoreresult_set.all()
        blue_results = results[0]
        red_results = results[1]

        output = {}
        output['red_results'] = red_results
        output['blue_results'] = blue_results

        return output