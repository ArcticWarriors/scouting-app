'''
Created on Mar 5, 2017

@author: PJ
'''
from BaseScouting.api_scraper.fake_data_scripts.CreateFakeJsonBase import CreateFakeJsonBase
import collections


class CreateFakeJson_BlueAlliance(CreateFakeJsonBase):

    def __init__(self, year, competition, match_model, official_match_model, official_match_sr_model):
        self.year = year
        CreateFakeJsonBase.__init__(self, competition, match_model, official_match_model, official_match_sr_model)
        pass

    def _populateAlliance(self, color, teams):
        return self._populate_score_breakdown(teams)

    def _prepare_match_info(self, match_number, score_breakdown, alliances):

        match_scores = collections.OrderedDict()
        match_scores['comp_level'] = "qm"
        match_scores['matchNumber'] = str(match_number)
        match_scores['videos'] = []
        match_scores['set_number'] = 1
        match_scores['score_breakdown'] = {"red": score_breakdown[0], "blue": score_breakdown[1]}
        match_scores['event_key'] = "%s%s" % (self.year, self.competition.code)

        alliance_info = {}
        for i, color in enumerate(alliances):
            teams = alliances[color]
            color = color.lower()
            alliance_info[color] = {}
            alliance_info[color]["surrogates"] = []
            alliance_info[color]["score"] = score_breakdown[i]["totalPoints"]
            alliance_info[color]["teams"] = ["frc%s" % team.teamNumber for team in teams]

        match_scores['alliances'] = alliance_info

        return match_scores

    def _create_match(self, match, official_match_srs, robots):
        output = CreateFakeJsonBase._create_match(self, match, official_match_srs, robots)

        return output
