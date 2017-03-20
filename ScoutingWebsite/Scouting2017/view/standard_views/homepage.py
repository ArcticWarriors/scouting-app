from BaseScouting.views.standard_views.base_homepage import BaseHomepageView
from Scouting2017.model.reusable_models import Competition, Match, Team, \
    OfficialMatch
from Scouting2017.model.predict_match import predict_match


class HomepageView2017(BaseHomepageView):

    def __init__(self):
        BaseHomepageView.__init__(self, Competition, Team, Match, OfficialMatch, 'BaseScouting/index.html')

    def _get_our_team_number(self):
        return 174

    def _get_our_metrics(self, competition):

        return None

    def _get_competition_metrics(self, competition):

        return None

    def _predict_match(self, match, competition):

        output = predict_match(match, competition)

        if output != None:
            output['matchNumber'] = match.matchNumber

        return output
