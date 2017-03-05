'''
Created on Mar 8, 2016

@author: PJ
'''
from BaseScouting.api_scraper.the_blue_alliance.PopulateResultsFromApi import PopulateResultsFromApi
from Scouting2017.api_scraper.PopulateRegionalResultsMixin import PopulateRegionalResultsMixin


class PopulateResultsFromApi2017(PopulateRegionalResultsMixin, PopulateResultsFromApi,):

    def __init__(self):
        from Scouting2017.model import Team, Match, Competition, OfficialMatch, OfficialMatchScoreResult, TeamCompetesIn
        PopulateResultsFromApi.__init__(self, Team, TeamCompetesIn, Match, Competition, OfficialMatch, OfficialMatchScoreResult)
