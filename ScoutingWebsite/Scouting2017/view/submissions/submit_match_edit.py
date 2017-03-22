'''
Created on Mar 1, 2017

@author: PJ
'''
from BaseScouting.views.submissions.submit_match_edit import BaseSubmitMatchEdit
from Scouting2017.model import OfficialMatch, Competition, Match, Team, ScoreResult
from Scouting2017.model.validate_match import calculate_match_scouting_validity


class SubmitMatchEdit2017(BaseSubmitMatchEdit):

    def __init__(self):
        BaseSubmitMatchEdit.__init__(self, Competition, Match, Team, ScoreResult, OfficialMatch)

    def _recalculate_official_results_validity(self, match, official_match, official_sr_search):

        error_level, red_missing, blue_missing, duplicate_teams, extra_teams, warning_messages, error_messages = calculate_match_scouting_validity(match, official_match, official_sr_search)

        missing_teams = red_missing.union(blue_missing)
        if len(missing_teams) != 0:
            error_messages.append(("Missing Teams", ", ".join([str(team.teamNumber) for team in missing_teams]), ""))

        if len(duplicate_teams) != 0:
            error_messages.append(("Duplicate Teams", ", ".join([str(team.teamNumber) for team in duplicate_teams]), ""))

        if len(extra_teams) != 0:
            error_messages.append(("Extra Teams", ", ".join([str(team.teamNumber) for team in extra_teams]), ""))

        return error_level, warning_messages, error_messages
