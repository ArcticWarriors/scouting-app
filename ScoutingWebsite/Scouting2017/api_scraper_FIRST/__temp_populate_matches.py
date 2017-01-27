'''
Created on Mar 1, 2016

@author: PJ
'''
import collections
import random
import sys
import os
import subprocess
from BaseScouting.load_django import load_django


def getRandomNumber(minval, maxval):
    return range(minval, maxval + 1)[random.randint(minval, maxval)]


def getPotentiallyWrongNumber(scouted_number, accuracy, subtracted_number, added_number, min_value, max_value):

    output = scouted_number
    
    rando = random.randint(0, 100)
    if rando > accuracy:
        high_or_low = random.randint(0, 1)
        if high_or_low == 0:
            fudge_factor = -random.randint(0, min_value)
        else:
            fudge_factor = random.randint(0, max_value)
        
        output += fudge_factor
        output = max(output, min_value)
        output = min(output, max_value)
    
    return output



def create_score_result(scouted_match, team):
    from Scouting2017.model import ScoreResult
    from Scouting2017.model.reusable_models import TeamCompetesIn
    
    scouted_sr = ScoreResult.objects.get_or_create(team=team, match=scouted_match, competition=scouted_match.competition)[0]
    
    
    
    # Teleop
    scouted_sr.gears_score         = getRandomNumber(0, 1)
    scouted_sr.fuel_shot_hi        = getRandomNumber(0, 120)
    scouted_sr.fuel_shot_low       = getRandomNumber(0, 120)
    scouted_sr.fuel_score_hi       = getRandomNumber(0, 80)
    scouted_sr.fuel_score_low      = getRandomNumber(0, 80)
    scouted_sr.rope                = getRandomNumber(0, 1)
    scouted_sr.hopper              = getRandomNumber(0, 1)
    
    # Fouls
    scouted_sr.tech_foul           = getRandomNumber(0, 1)
    scouted_sr.foul                = getRandomNumber(0, 1)
    scouted_sr.red_card            = getRandomNumber(0, 1)
    scouted_sr.yellow_card         = getRandomNumber(0, 1)
    
    # Auto
    scouted_sr.fuel_shot_hi_auto   = getRandomNumber(0, 10)
    scouted_sr.fuel_shot_low_auto  = getRandomNumber(0, 10)
    scouted_sr.fuel_score_hi_auto  = getRandomNumber(0, 10)
    scouted_sr.fuel_score_low_auto = getRandomNumber(0, 10)
    scouted_sr.gears_score_auto    = getRandomNumber(0, 1)
    scouted_sr.baseline            = getRandomNumber(0, 1)
    
    # Fuel
    scouted_sr.ground_fuel         = getRandomNumber(0, 1)
    scouted_sr.ground_gear         = getRandomNumber(0, 1)
    
    scouted_sr.save()


def reset_official_result(official_sr):
    official_sr.auto_gears      = 0
    official_sr.auto_fuel_high  = 0
    official_sr.auto_fuel_low   = 0
    official_sr.auto_baseline   = 0
    official_sr.fuel_high       = 0
    official_sr.fuel_low        = 0
    official_sr.takeoffs        = 0


def update_official_result(official_sr, scouted_sr):
    
    official_sr.auto_gears      += getPotentiallyWrongNumber(scouted_sr.gears_score_auto, 90, 1, 0, 0, 1)
    official_sr.auto_fuel_high  += getPotentiallyWrongNumber(scouted_sr.fuel_score_hi_auto, 60, 1, 4, 2, 10)
    official_sr.auto_fuel_low   += getPotentiallyWrongNumber(scouted_sr.fuel_score_low_auto, 60, 1, 4, 2, 10)
    official_sr.auto_baseline   += getPotentiallyWrongNumber(1 if scouted_sr.baseline else 0, 90, 1, 1, 0, 1)
    
    official_sr.fuel_high       += getPotentiallyWrongNumber(scouted_sr.fuel_score_hi, 90, 1, 30, 20, 120)
    official_sr.fuel_low        += getPotentiallyWrongNumber(scouted_sr.fuel_score_low, 90, 1, 30, 20, 120)
    official_sr.takeoffs        += getPotentiallyWrongNumber(1 if scouted_sr.rope else 0, 98, 1, 1, 0, 1)


def main():
    
    match_nums_to_do = range(1, 40)
    
    random.seed(100)
    
    from Scouting2017.model import OfficialMatch, Match, OfficialMatchScoreResult
    
    print "Updating scouting matches..."
    for match_num in match_nums_to_do:
        official_match = OfficialMatch.objects.get(matchNumber=match_num)
        scouted_match = Match.objects.get_or_create(matchNumber=match_num, competition=official_match.competition)[0]
         
        print "  Match #%s" % match_num
          
        for official_sr in OfficialMatchScoreResult.objects.filter(official_match=official_match):
            create_score_result(scouted_match, official_sr.team1)
            create_score_result(scouted_match, official_sr.team2)
            create_score_result(scouted_match, official_sr.team3)

    print "Updating official score results..."
    for official_match in OfficialMatch.objects.all():
#         print official_match
        scouted_match = Match.objects.filter(matchNumber=official_match.matchNumber, competition=official_match.competition)
        official_sr = OfficialMatchScoreResult.objects.filter(official_match=official_match)

        if len(scouted_match) != 1:
            continue
        
        if len(official_sr) != 2:
            continue
        
        print "  Match #%s" % official_match.matchNumber
        
        scouted_match = scouted_match[0]
        match_srs = scouted_match.scoreresult_set.all()
        official_blue = official_sr[0]
        official_red = official_sr[1]
        
        reset_official_result(official_blue)
        reset_official_result(official_red)
        
        for i in range(0, 3):
            update_official_result(official_blue, match_srs[i])
            
        for i in range(3, 6):
            update_official_result(official_red, match_srs[i])

        official_blue.save()
        official_red.save()
        official_match.save()


if __name__ == "__main__":
    load_django()
    main()