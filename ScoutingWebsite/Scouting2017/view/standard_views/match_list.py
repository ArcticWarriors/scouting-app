from BaseScouting.views.standard_views.base_match_list import BaseMatchListView
from Scouting2017.model.reusable_models import Match, OfficialMatch
from Scouting2017.model.validate_match import calculate_match_scouting_validity


class MatchListView2017(BaseMatchListView):
    def __init__(self):
        BaseMatchListView.__init__(self, Match)

    def _append_scouted_info(self, match, regional_code):

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
            if len(official_sr_search) == 2:
                red_score = official_sr_search[0].totalPoints
                blue_score = official_sr_search[1].totalPoints

                output.redScore = red_score
                output.blueScore = blue_score

                if red_score > blue_score:
                    output.winning_alliance = "Red"
                elif blue_score > red_score:
                    output.winning_alliance = "Blue"
                else:
                    output.winning_alliance = "Tie"

            output.match_error_level, output.match_error_warning_messages, output.match_error_error_messages = calculate_match_scouting_validity(match, official_match, official_sr_search)

        return output
