from BaseScouting.views.standard_views.base_match_list import BaseMatchListView
from Scouting2017.model.reusable_models import Match, OfficialMatch, Competition
from Scouting2017.model.validate_match import calculate_match_scouting_validity
from Scouting2017.model.predict_match import predict_match


class MatchListView2017(BaseMatchListView):
    def __init__(self):
        BaseMatchListView.__init__(self, 2017, Match)

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

            output.match_error_level, _, _, _, _, output.match_error_warning_messages, output.match_error_error_messages = calculate_match_scouting_validity(match, official_match, official_sr_search)

        return output

    def _append_unscouted_info(self, match, regional_code):
        match_prediction = predict_match(match, Competition.objects.get(code=regional_code))

        official_match_search = OfficialMatch.objects.filter(competition__code=regional_code, matchNumber=match.matchNumber)

        output = match

        if len(official_match_search) == 0 or not official_match_search[0].hasOfficialData:
            output.isPrediction = True
            output.redScore = "{0:.2f}".format(match_prediction["red_prediction"]["total_score"] if "total_score" in match_prediction["red_prediction"] else 0)
            output.blueScore = "{0:.2f}".format(match_prediction["blue_prediction"]["total_score"] if "total_score" in match_prediction["blue_prediction"] else 0)
        else:
            official_match = official_match_search[0]
            official_sr_search = official_match.officialmatchscoreresult_set.all()
            output.isPrediction = False
            if len(official_sr_search) == 2:

                output.redScore = official_sr_search[0].totalPoints
                output.blueScore = official_sr_search[1].totalPoints

        return output
