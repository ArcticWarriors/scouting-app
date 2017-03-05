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
