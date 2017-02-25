'''
Created on Mar 1, 2016

@author: PJ
'''
from BaseScouting.api_scraper_FIRST.TempRetrofilSrFromOfficialResults import TempRetrofillSrFromOfficialResults
from BaseScouting.load_django import load_django


class TempRetrofillSrFromOfficialResults2017(TempRetrofillSrFromOfficialResults):
    
    gear_lookup = {
                  0: 0,
                  1: 1,
                  2: 3,
                  3: 7,
                  4: 13,
                  }
    
    def __get_common_fields(self, official_match_sr):
        output = {}
        
        auto_rotor_count = official_match_sr.rotor1Auto + official_match_sr.rotor2Auto
        tele_rotor_count = official_match_sr.rotor1Engaged + official_match_sr.rotor2Engaged + official_match_sr.rotor3Engaged + official_match_sr.rotor4Engaged
        
        output['baseline'] = 0
        output['foul']                = int(official_match_sr.foulCount / 3.0)
        output['fuel_score_hi']       = int(official_match_sr.teleopFuelHigh / 3.0)
        output['fuel_score_hi_auto']  = int(official_match_sr.autoFuelHigh / 3.0)
        output['fuel_score_low']      = int(official_match_sr.teleopFuelLow / 3.0)
        output['fuel_score_low_auto'] = int(official_match_sr.autoFuelLow / 3.0)
        output['gears_score']         = int(self.gear_lookup[tele_rotor_count] / 3.0)
        output['gears_score_auto']    = int(self.gear_lookup[auto_rotor_count] / 3.0)
        
        output['fuel_shot_hi'] = output['fuel_score_hi']
        output['fuel_shot_hi_auto'] = output['fuel_score_hi_auto']
        output['fuel_shot_low'] = output['fuel_score_low']
        output['fuel_shot_low_auto'] = output['fuel_score_low_auto']
    
        return output
    
    def get_team1_stats(self, official_match_sr):
        output = self.__get_common_fields(official_match_sr)
        
        output['baseline']  = official_match_sr.robot1Auto == "Mobility"
        output['rope']      = official_match_sr.touchpadFar == 1
        output['foul']      = official_match_sr.foulCount >= 1
        output['tech_foul'] = official_match_sr.techFoulCount >= 1
    
        return output
        
    def get_team2_stats(self, official_match_sr):
        output = self.__get_common_fields(official_match_sr)
        
        output['baseline']  = official_match_sr.robot2Auto == "Mobility"
        output['rope']      = official_match_sr.touchpadMiddle == 1
        output['foul']      = official_match_sr.foulCount >= 2
        output['tech_foul'] = official_match_sr.techFoulCount >= 2
    
        return output
        
    def get_team3_stats(self, official_match_sr):
        output = self.__get_common_fields(official_match_sr)
        
        output['baseline']  = official_match_sr.robot3Auto == "Mobility"
        output['rope']      = official_match_sr.touchpadNear == 1
        output['foul']      = official_match_sr.foulCount >= 3
        output['tech_foul'] = official_match_sr.techFoulCount >= 3
    
        return output


def retrofill_results(min_match_number, max_match_number):
    from Scouting2017.model.reusable_models import OfficialMatch, Match
    from Scouting2017.model.models2017 import OfficialMatchScoreResult, ScoreResult
    

    populater = TempRetrofillSrFromOfficialResults2017()
    
    for match_number in range(min_match_number, max_match_number):
        official_matches = OfficialMatch.objects.filter(matchNumber=match_number)
        if len(official_matches) != 1:
            continue
        
        official_match = official_matches[0]
        official_srs = OfficialMatchScoreResult.objects.filter(official_match=official_match)
        print official_srs[0]
        print official_srs
        match, _ = Match.objects.get_or_create(matchNumber=official_match.matchNumber)
        
        populater.populate_matchresults(official_match, Match, ScoreResult, OfficialMatchScoreResult)

if __name__ == "__main__":
    load_django()
    retrofill_results(1, 40)