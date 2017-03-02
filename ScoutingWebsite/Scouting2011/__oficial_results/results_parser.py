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

with open(r'C:\Users\PJ\GitHub\SnobotScouting\scouting-app\ScoutingWebsite\Scouting2011\__oficial_results\spbli_results.txt') as f:

    for line in f.readlines():
        parts = line.strip().split("\t")

        match_number = int(parts[0][parts[0].find(" "):])
        official_match, _ = OfficialMatch.objects.get_or_create(matchNumber=match_number, competition=competition)

        official_sr_search = OfficialMatchScoreResult.objects.filter(competition=competition, official_match=official_match)
        
        match_search = Match.objects.filter(matchNumber=match_number)
        if len(match_search) == 1:
            match = match_search[0]
            print match
        else:
            print "UH OH"
        
        
        if len(official_sr_search) != 2:

            red1 = int(parts[2])
            red2 = int(parts[3])
            red3 = int(parts[4])
    
            blue1 = int(parts[5])
            blue2 = int(parts[6])
            blue3 = int(parts[7])
    
            red_score = int(parts[8])
            blue_score = int(parts[9])
    
            OfficialMatchScoreResult.objects.create(competition=competition,
                                                    official_match=official_match,
                                                    team1=Team.objects.get(teamNumber=red1),
                                                    team2=Team.objects.get(teamNumber=red2),
                                                    team3=Team.objects.get(teamNumber=red3),
                                                    total_score=red_score)
    
            OfficialMatchScoreResult.objects.create(competition=competition,
                                                    official_match=official_match,
                                                    team1=Team.objects.get(teamNumber=blue1),
                                                    team2=Team.objects.get(teamNumber=blue2),
                                                    team3=Team.objects.get(teamNumber=blue3),
                                                    total_score=blue_score)
#         print match_number
