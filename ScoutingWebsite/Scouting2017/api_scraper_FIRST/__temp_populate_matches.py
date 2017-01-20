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


def randomNumber(minval, maxval):
    return range(minval, maxval + 1)[random.randint(minval, maxval)]


def create_score_result(scouted_match, team):
    from Scouting2017.model import ScoreResult
    
    scouted_sr = ScoreResult.objects.get_or_create(team=team, match=scouted_match, competition=scouted_match.competition)[0]
    
    # Teleop
    scouted_sr.gears_score         = randomNumber(0, 1)
    scouted_sr.fuel_shot_hi        = randomNumber(0, 120)
    scouted_sr.fuel_shot_low       = randomNumber(0, 120)
    scouted_sr.fuel_score_hi       = randomNumber(0, 80)
    scouted_sr.fuel_score_low      = randomNumber(0, 80)
    scouted_sr.rope                = randomNumber(0, 1)
    scouted_sr.hopper              = randomNumber(0, 1)
    
    # Fouls
    scouted_sr.tech_foul           = randomNumber(0, 1)
    scouted_sr.foul                = randomNumber(0, 1)
    scouted_sr.red_card            = randomNumber(0, 1)
    scouted_sr.yellow_card         = randomNumber(0, 1)
    
    # Auto
    scouted_sr.fuel_shot_hi_auto   = randomNumber(0, 10)
    scouted_sr.fuel_shot_low_auto  = randomNumber(0, 10)
    scouted_sr.fuel_score_hi_auto  = randomNumber(0, 10)
    scouted_sr.fuel_score_low_auto = randomNumber(0, 10)
    scouted_sr.gears_score_auto    = randomNumber(0, 1)
    scouted_sr.baseline            = randomNumber(0, 1)
    
    # Fuel
    scouted_sr.ground_fuel         = randomNumber(0, 1)
    scouted_sr.ground_gear         = randomNumber(0, 1)
    
    scouted_sr.save()


def main():
    
    match_nums_to_do = range(1, 40)
    
    random.seed(100)
    
    from Scouting2017.model import OfficialMatch, Match, OfficialMatchScoreResult
    
    for match_num in match_nums_to_do:
        official_match = OfficialMatch.objects.get(matchNumber=match_num)
        scouted_match = Match.objects.get_or_create(matchNumber=match_num, competition=official_match.competition)[0]
        
        for official_sr in OfficialMatchScoreResult.objects.filter(official_match=official_match):
            create_score_result(scouted_match, official_sr.team1)
            create_score_result(scouted_match, official_sr.team2)
            create_score_result(scouted_match, official_sr.team3)
    
    pass


if __name__ == "__main__":
    load_django()
    main()