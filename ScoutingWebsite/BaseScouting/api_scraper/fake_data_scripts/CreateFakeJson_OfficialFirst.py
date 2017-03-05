'''
Created on Mar 5, 2017

@author: PJ
'''
from BaseScouting.api_scraper.fake_data_scripts.CreateFakeJsonBase import CreateFakeJsonBase
import collections


class CreateFakeJson_OfficialFirst(CreateFakeJsonBase):

    def _populateAlliance(self, color, teams):
        output = collections.OrderedDict()
        output["alliance"] = color
        output.update(self._populate_score_breakdown(teams))

        return output

    def _prepare_match_info(self, match_number, score_breakdown, alliances):

        match_scores = collections.OrderedDict()
        match_scores['matchLevel'] = "Qualification"
        match_scores['Alliances'] = score_breakdown
        match_scores['matchNumber'] = str(match_number)

        return match_scores

    def _create_match(self, match, official_match_srs, robots):
        output = CreateFakeJsonBase._create_match(self, match, official_match_srs, robots)

        return output
