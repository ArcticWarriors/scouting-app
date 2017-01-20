'''
Created on Mar 8, 2016

@author: PJ
'''

from BaseScouting.api_scraper_FIRST.PopulateResultsFromApi import PopulateRegionalResults


class PopulateRegionalresults2017(PopulateRegionalResults):

    def __init__(self):
        from Scouting2017.model import Team, Competition, OfficialMatch, OfficialMatchScoreResult
        PopulateRegionalResults.__init__(self, Team, Competition, OfficialMatch, OfficialMatchScoreResult)

    def populate_official_sr(self, official_match_sr, alliance_info):

        official_match_sr.save()
