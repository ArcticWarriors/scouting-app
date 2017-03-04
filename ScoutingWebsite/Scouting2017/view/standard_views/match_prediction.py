from BaseScouting.views.base_views import BaseMatchPredictionView
from Scouting2017.model.reusable_models import Match, Competition
from Scouting2017.model.predict_match import predict_match


class MatchPredictionView2017(BaseMatchPredictionView):
    def __init__(self):
        BaseMatchPredictionView.__init__(self, Match, 'Scouting2017/match_prediction.html')

    def get_score_results(self, match, regional_code):

        return predict_match(match, Competition.objects.get(code=regional_code))
