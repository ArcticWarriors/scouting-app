'''
Created on Feb 26, 2017

@author: PJ
'''
import os
from BaseScouting.load_django import load_django

load_django()
from Scouting2016.model import TeamPictures, Team, Competition, Match, OfficialMatch


competition = Competition.objects.get(code="NYRO")


for official_match in OfficialMatch.objects.filter(competition=competition):
    match_search = Match.objects.filter(matchNumber=official_match.matchNumber)
    if len(match_search) == 1:
        match = match_search[0]
        official_srs = official_match.officialmatchscoreresult_set.all()
        red_official = official_srs[0]
        blue_official = official_srs[1]
        
        match.red1 = red_official.team1
        match.red2 = red_official.team2
        match.red3 = red_official.team3
        
        match.blue1 = blue_official.team1
        match.blue2 = blue_official.team2
        match.blue3 = blue_official.team3
        
        match.save()
#     print match_search

print competition