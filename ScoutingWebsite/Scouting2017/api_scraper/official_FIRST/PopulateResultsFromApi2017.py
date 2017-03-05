'''
Created on Mar 8, 2016

@author: PJ
'''

from BaseScouting.api_scraper.official_FIRST.PopulateResultsFromApi import PopulateRegionalResults
from Scouting2017.api_scraper.PopulateRegionalResultsMixin import PopulateRegionalResultsMixin


class PopulateRegionalresults2017(PopulateRegionalResults, PopulateRegionalResultsMixin):

    def __init__(self):
        from Scouting2017.model import Team, Match, Competition, OfficialMatch, OfficialMatchScoreResult, TeamCompetesIn
        PopulateRegionalResults.__init__(self, Team, TeamCompetesIn, Match, Competition, OfficialMatch, OfficialMatchScoreResult)
