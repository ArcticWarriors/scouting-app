from BaseScouting.views.base_views import BaseSingleMatchView
from Scouting2011.model.reusable_models import Match, OfficialMatch
from Scouting2011.model.models2011 import ScoreResult
from Scouting2011.model.validate_match import validate_match

class SingleMatchView2011(BaseSingleMatchView):

    def __init__(self):
        BaseSingleMatchView.__init__(self, Match, 'Scouting2011/view_match.html')

    def get_metrics(self, sr):
        output = []
        output.append(('teamNumber', sr.team.teamNumber))
        sr_fields = ScoreResult.get_fields()
        for key in sr_fields:
            sr_field = sr_fields[key]
            output.append((sr_field.display_name, getattr(sr, key)))

        return output
    
    def get_match_validation(self, regional_code, match):

        official_match_search = OfficialMatch.objects.filter(competition__code=regional_code, matchNumber=match.matchNumber)

        if len(official_match_search) == 1:
            official_match = official_match_search[0]
            official_sr_search = official_match.officialmatchscoreresult_set.all()
            if len(official_sr_search) == 2:
                _, warnings, errors = validate_match(match, official_match, official_sr_search)

                return True, warnings, errors

        return False, [], []
