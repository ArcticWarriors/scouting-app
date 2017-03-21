from BaseScouting.views.standard_views.base_match import BaseSingleMatchView
from Scouting2017.model.reusable_models import Match, OfficialMatch
from Scouting2017.model.validate_match import calculate_match_scouting_validity
import collections


class SingleMatchView2017(BaseSingleMatchView):

    def __init__(self):
        BaseSingleMatchView.__init__(self, Match, 'Scouting2017/match.html')

    def get_sr(self, team, match):

        sr_search = team.scoreresult_set.filter(match=match)
        if len(sr_search) == 1:
            return sr_search[0]

        return None

    def get_context_data(self, **kwargs):
        context = BaseSingleMatchView.get_context_data(self, **kwargs)

        match = context['match']

        context['alliances'] = collections.OrderedDict()

        context['alliances']['Red'] = {}
        context['alliances']['Red']['score_results'] = []
        context['alliances']['Red']['score_results'].append(self.get_sr(match.red1, match))
        context['alliances']['Red']['score_results'].append(self.get_sr(match.red2, match))
        context['alliances']['Red']['score_results'].append(self.get_sr(match.red3, match))

        context['alliances']['Blue'] = {}
        context['alliances']['Blue']['score_results'] = []
        context['alliances']['Blue']['score_results'].append(self.get_sr(match.blue1, match))
        context['alliances']['Blue']['score_results'].append(self.get_sr(match.blue2, match))
        context['alliances']['Blue']['score_results'].append(self.get_sr(match.blue3, match))

        return context

    def get_metrics(self, score_result):
        return []

    def get_match_validation(self, regional_code, match):

        official_match = OfficialMatch.objects.get(matchNumber=match.matchNumber, competition__code=regional_code)
        official_sr_search = official_match.officialmatchscoreresult_set.all()
        if len(official_sr_search) == 2:
            _, warnings, errors = calculate_match_scouting_validity(match, official_match, official_sr_search)

            return True, warnings, errors

        return False, [], []
