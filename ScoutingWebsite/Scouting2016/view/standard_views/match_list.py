from BaseScouting.views.base_views import BaseMatchListView
from Scouting2016.model.reusable_models import Match, OfficialMatch
from Scouting2016.model.models2016 import validate_match


class MatchListView2016(BaseMatchListView):

    def __init__(self):
        BaseMatchListView.__init__(self, Match, template_name='Scouting2016/match_list.html')

    def append_scouted_info(self, match, regional_code):

        output = match

        output.match_error_level = 0
        output.match_error_warning_messages = []
        output.match_error_error_messages = []
        output.winning_alliance = "Unofficial"
        output.redScore = "Unknown"
        output.blueScore = "Unknown"

        official_match_search = OfficialMatch.objects.filter(competition__code=regional_code, matchNumber=match.matchNumber)
        if len(official_match_search) == 1:
            official_match = official_match_search[0]
            official_sr_search = official_match.officialmatchscoreresult_set.all()
            output.match_error_level, output.match_error_warning_messages, output.match_error_error_messages = validate_match(match, official_match, official_sr_search)

        return output
