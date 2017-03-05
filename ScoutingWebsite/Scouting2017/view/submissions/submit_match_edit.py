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
        return calculate_match_scouting_validity(match, official_match, official_sr_search)
