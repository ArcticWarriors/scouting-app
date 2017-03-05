from BaseScouting.views.base_views import BaseMatchPredictionView
from Scouting2011.model.reusable_models import Match, Competition
from Scouting2011.model.predict_match import predict_match


class OfficialMatchView2011(BaseMatchPredictionView):

    def __init__(self):
        BaseMatchPredictionView.__init__(self, Match, Competition, 'BaseScouting/match_prediction.html')

    def get_score_results(self, match, competition):
        return predict_match(match, competition)
