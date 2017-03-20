from BaseScouting.views.standard_views.base_match_prediction import BaseMatchPredictionView
from Scouting2017.model.reusable_models import Match, Competition
from Scouting2017.model.predict_match import predict_match


class MatchPredictionView2017(BaseMatchPredictionView):
    def __init__(self):
        BaseMatchPredictionView.__init__(self, Match, Competition, 'Scouting2017/match_prediction.html')

    def get_score_results(self, match, competition):

        return predict_match(match, competition)
