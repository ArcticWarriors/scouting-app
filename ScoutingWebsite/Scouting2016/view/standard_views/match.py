from BaseScouting.views.base_views import BaseSingleMatchView
from Scouting2016.model.reusable_models import Match, OfficialMatch
from Scouting2016.model.models2016 import validate_match


class SingleMatchView2016(BaseSingleMatchView):

    def __init__(self):
        BaseSingleMatchView.__init__(self, Match, 'Scouting2016/match.html')

    def get_metrics(self, score_result):
        return []

    def get_match_validation(self, regional_code, match):

        official_match_search = OfficialMatch.objects.filter(competition__code=regional_code, matchNumber=match.matchNumber)

        if False:
            official_match = official_match_search[0]
            official_sr_search = official_match.officialmatchscoreresult_set.all()
            if len(official_sr_search) == 2:
                _, warnings, errors = validate_match(match, official_match, official_sr_search)

                return True, warnings, errors

        return False, [], []
