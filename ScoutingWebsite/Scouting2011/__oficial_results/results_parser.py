'''
Created on Mar 2, 2017

@author: PJ
'''
from BaseScouting.load_django import load_django


load_django()

from Scouting2011.model.reusable_models import OfficialMatch, Competition, Team,\
    Match
from Scouting2011.model.models2011 import OfficialMatchScoreResult

competition = Competition.objects.get(id=1)

with open(r'spbli_results.txt') as f:

    for line in f.readlines():
        parts = line.strip().split("\t")

        match_number = int(parts[0][parts[0].find(" "):])
        official_match, _ = OfficialMatch.objects.get_or_create(matchNumber=match_number, competition=competition)

        official_sr_search = OfficialMatchScoreResult.objects.filter(competition=competition, official_match=official_match)
        
        red1 = Team.objects.get(teamNumber=int(parts[2]))
        red2 = Team.objects.get(teamNumber=int(parts[3]))
        red3 = Team.objects.get(teamNumber=int(parts[4]))

        blue1 = Team.objects.get(teamNumber=int(parts[5]))
        blue2 = Team.objects.get(teamNumber=int(parts[6]))
        blue3 = Team.objects.get(teamNumber=int(parts[7]))
        
        match_search = Match.objects.filter(matchNumber=match_number)
        if len(match_search) == 1:
            match = match_search[0]
            match.red1 = red1
            match.red2 = red2
            match.red3 = red3
            match.blue1 = blue1
            match.blue2 = blue2
            match.blue3 = blue3
            match.save()
        else:
            match = Match.objects.create(competition=competition, matchNumber=match_number, red1=red1, red2=red2, red3=red3, blue1=blue1, blue2=blue2, blue3=blue3)
        
#         if create_match:
#             print Match.objects.create(competition=competition, matchNumber=match_number, red1=red1, red2=red2, red3=red3, blue1=blue1, blue2=blue2, blue3=blue3)
        
        if len(official_sr_search) != 2:

    
            red_score = int(parts[8])
            blue_score = int(parts[9])
            
                
    
            OfficialMatchScoreResult.objects.create(competition=competition,
                                                    official_match=official_match,
                                                    team1=red1,
                                                    team2=red2,
                                                    team3=red3,
                                                    total_score=red_score)
    
            OfficialMatchScoreResult.objects.create(competition=competition,
                                                    official_match=official_match,
                                                    team1=blue1,
                                                    team2=blue2,
                                                    team3=blue3,
                                                    total_score=blue_score)
#         print match_number
