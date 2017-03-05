from BaseScouting.views.base_views import BaseSingleMatchView
from Scouting2013.model.reusable_models import Match
from Scouting2013.model.models2013 import ScoreResult


class SingleMatchView2013(BaseSingleMatchView):

    def __init__(self):
        BaseSingleMatchView.__init__(self, Match, 'Scouting2013/view_match.html')

    def get_metrics(self, sr):
        output = []
        output.append(('teamNumber', sr.team.teamNumber))
        sr_fields = ScoreResult.get_fields()
        for key in sr_fields:
            sr_field = sr_fields[key]
            output.append((sr_field.display_name, getattr(sr, key)))

        return output