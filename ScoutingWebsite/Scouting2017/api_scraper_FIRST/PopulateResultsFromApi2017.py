'''
Created on Mar 8, 2016

@author: PJ
'''

from BaseScouting.api_scraper_FIRST.PopulateResultsFromApi import PopulateRegionalResults


class PopulateRegionalresults2017(PopulateRegionalResults):

    def __init__(self):
        from Scouting2017.model import Team, Match, Competition, OfficialMatch, OfficialMatchScoreResult
        PopulateRegionalResults.__init__(self, Team, Match, Competition, OfficialMatch, OfficialMatchScoreResult)

    def populate_official_sr(self, official_match_sr, alliance_info):
        
        official_match_sr.alliance_color = alliance_info['alliance'][0]
        official_match_sr.robot1Auto = alliance_info['robot1Auto']
        official_match_sr.robot2Auto = alliance_info['robot2Auto']
        official_match_sr.robot3Auto = alliance_info['robot3Auto']
        official_match_sr.autoFuelLow = alliance_info['autoFuelLow']
        official_match_sr.autoFuelHigh = alliance_info['autoFuelHigh']
        official_match_sr.rotor1Auto = alliance_info['rotor1Auto']
        official_match_sr.rotor2Auto = alliance_info['rotor2Auto']
        official_match_sr.teleopFuelLow = alliance_info['teleopFuelLow']
        official_match_sr.teleopFuelHigh = alliance_info['teleopFuelHigh']
        official_match_sr.rotor1Engaged = alliance_info['rotor1Engaged']
        official_match_sr.rotor2Engaged = alliance_info['rotor2Engaged']
        official_match_sr.rotor3Engaged = alliance_info['rotor3Engaged']
        official_match_sr.rotor4Engaged = alliance_info['rotor4Engaged']
        official_match_sr.touchpadNear = alliance_info['touchpadNear']
        official_match_sr.touchpadMiddle = alliance_info['touchpadMiddle']
        official_match_sr.touchpadFar = alliance_info['touchpadFar']
        official_match_sr.foulCount = alliance_info['foulCount']
        official_match_sr.techFoulCount = alliance_info['techFoulCount']
        official_match_sr.autoMobilityPoints = alliance_info['autoMobilityPoints']
        official_match_sr.autoRotorPoints = alliance_info['autoRotorPoints']
        official_match_sr.autoPoints = alliance_info['autoPoints']
        official_match_sr.teleopFuelPoints = alliance_info['teleopFuelPoints']
        official_match_sr.teleopRotorPoints = alliance_info['teleopRotorPoints']
        official_match_sr.teleopTakeoffPoints = alliance_info['teleopTakeoffPoints']
        official_match_sr.teleopPoints = alliance_info['teleopPoints']
        official_match_sr.foulPoints = alliance_info['foulPoints']
        official_match_sr.totalPoints = alliance_info['totalPoints']
        official_match_sr.kPaRankingPointAchieved = alliance_info['kPaRankingPointAchieved']
        official_match_sr.rotorRankingPointAchieved = alliance_info['rotorRankingPointAchieved']

        official_match_sr.save()
