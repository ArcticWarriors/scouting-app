from BaseScouting.views.base_views import BaseMatchPredictionView
from Scouting2016.model.reusable_models import OfficialMatch
from Scouting2016.model.models2016 import get_defense_stats
import operator


class OfficialMatchView2016(BaseMatchPredictionView):

    def __init__(self):
        BaseMatchPredictionView.__init__(self, OfficialMatch, 'Scouting2016/official_match.html')

    def __get_sorted_defense_stats(self, official_score_result):
        results = {}

        get_defense_stats(official_score_result.team1, results)
        get_defense_stats(official_score_result.team2, results)
        get_defense_stats(official_score_result.team3, results)

        for category in results:
            results[category] = sorted(results[category].items(), key=operator.itemgetter(1), reverse=True)

        return sorted(results.items())

    def get_score_results(self, official_match):

        results = official_match.officialmatchscoreresult_set.all()
        blue_results = results[0]
        red_results = results[1]

        output = {}
        output['red_results'] = red_results
        output['blue_results'] = blue_results

        output['red_defenses'] = self.__get_sorted_defense_stats(red_results)
        output['blue_defenses'] = self.__get_sorted_defense_stats(blue_results)

        return output
