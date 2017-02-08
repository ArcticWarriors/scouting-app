'''
Created on Feb 7, 2017

@author: PJ
'''
import random
import json
import collections
import math
from BaseScouting.load_django import load_django


class Robot:
    
    def __init__(self,
                 auto_mobility_percentage = 95,
                 auto_gear_percentage = 40,
                 auto_high_goal_percentage = 0,
                 auto_high_goal_capacity = 10,
                 auto_low_goal_percentage = 0,
                 auto_low_goal_capacity = 10,
                 
                 climb_percentage = 50,
                 tele_low_goal_percentage = 0,
                 tele_low_goal_capacity = 0,
                 tele_high_goal_percentage = 0,
                 tele_high_goal_capacity = 0,
                 tele_gear_max = 2,
                 tele_gear_consistancy = 50,
                 
                 foul_percentage=5,
                 tech_foul_percentage=1):
        
        self.auto_auto_mobility_percentage = auto_mobility_percentage
        self.auto_gear_percentage = auto_gear_percentage
        self.auto_high_goal_percentage = auto_high_goal_percentage
        self.auto_high_goal_capacity = auto_high_goal_capacity
        self.auto_low_goal_percentage = auto_low_goal_percentage
        self.auto_low_goal_capacity = auto_low_goal_capacity
        
        self.climb_percentage = climb_percentage
        self.tele_low_goal_percentage = tele_low_goal_percentage
        self.tele_low_goal_capacity = tele_low_goal_capacity
        self.tele_high_goal_percentage = tele_high_goal_percentage
        self.tele_high_goal_capacity = tele_high_goal_capacity
        self.tele_gear_max = tele_gear_max
        self.tele_gear_consistancy = tele_gear_consistancy
        
        self.foul_percentage = foul_percentage
        self.tech_foul_percentage = tech_foul_percentage
        
        
    def create_score_result(self):
        
        output = {}
        output['auto_mobility'] = 'Mobility' if getBoolWithPercentage(self.auto_auto_mobility_percentage) else 'None'
        output['auto_gear'] = 1 if getBoolWithPercentage(self.auto_gear_percentage) else 0
        output['auto_fuel_high']  = math.floor(self.auto_high_goal_percentage * self.auto_high_goal_capacity * .01)
        output['auto_fuel_low'] = math.floor(self.auto_low_goal_percentage * self.auto_low_goal_capacity * .01)
        
        output['climbing'] = 1 if getBoolWithPercentage(self.climb_percentage) else 0
        output['tele_gear'] = math.floor(self.tele_gear_max * self.tele_gear_consistancy * .01)
        output['tele_fuel_high']  = math.floor(self.tele_high_goal_percentage * self.tele_high_goal_capacity * .01)
        output['tele_fuel_low'] = math.floor(self.tele_low_goal_percentage * self.tele_low_goal_capacity * .01)
        
        output['foul_percentage'] = 1 if getBoolWithPercentage(self.foul_percentage) else 0
        output['tech_foul_percentage'] = 1 if getBoolWithPercentage(self.tech_foul_percentage) else 0
        
        return output


def getBoolWithPercentage(percentage):
    rando = random.randint(0, 100)
    
    return rando < percentage
    


def getRandomNumber(minval, maxval):
    
    output_range = maxval - minval
    
    rando = random.randint(0, 100)
    output = math.floor(minval + rando * .01 * output_range)
    print output_range, output
    
    precentage = rando
    return precentage


def count_mobility(robot1, robot2, robot3):
    mobility_sum = 0
    
    mobility_sum += 1 if robot1 == "Mobility" else 0
    mobility_sum += 1 if robot2 == "Mobility" else 0
    mobility_sum += 1 if robot3 == "Mobility" else 0
    
    return mobility_sum



def populateAlliance(alliance, robot1sr, robot2sr, robot3sr):
    
    output = collections.OrderedDict()
    output['alliance'] = alliance

    autoGearSum = robot1sr['auto_gear'] + robot2sr['auto_gear'] + robot3sr['auto_gear']
    teleGearSum = robot1sr['tele_gear'] + robot2sr['tele_gear'] + robot3sr['tele_gear']
    
    #############
    # Auto
    #############
    output["robot1Auto"]   = robot1sr['auto_mobility']
    output["robot2Auto"]   = robot2sr['auto_mobility']
    output["robot3Auto"]   = robot3sr['auto_mobility']
    mobility_count = count_mobility(output["robot1Auto"], output["robot2Auto"], output["robot3Auto"])
    
    output["autoFuelLow"]  = robot1sr['auto_fuel_low'] + robot2sr['auto_fuel_low'] + robot3sr['auto_fuel_low']
    output["autoFuelHigh"] = robot1sr['auto_fuel_high'] + robot2sr['auto_fuel_high'] + robot3sr['auto_fuel_high']
    auto_fuel_kpa = output["autoFuelHigh"] + output["autoFuelLow"] / 3.0
    
    output["rotor1Auto"] = 1 if autoGearSum >= 1 else 0
    output["rotor2Auto"] = 1 if autoGearSum >= 3 else 0
    auto_rotor_count = output["rotor1Auto"] + output["rotor2Auto"]
     
    #############
    # Tele
    #############
    output["teleopFuelLow"] = robot1sr['tele_fuel_low'] + robot2sr['tele_fuel_low'] + robot3sr['tele_fuel_low']
    output["teleopFuelHigh"] = robot1sr['tele_fuel_high'] + robot2sr['tele_fuel_high'] + robot3sr['tele_fuel_high']
    teleop_fuel_kpa = output["teleopFuelLow"] / 3.0 + output["teleopFuelHigh"] / 9.0
    
    output["rotor1Engaged"] = max(0, (1 if teleGearSum >= 1  else 0) - output["rotor1Auto"])
    output["rotor2Engaged"] = max(0, (1 if teleGearSum >= 3  else 0) - output["rotor2Auto"])
    output["rotor3Engaged"] = 1 if teleGearSum >= 7  else 0
    output["rotor4Engaged"] = 1 if teleGearSum >= 13 else 0
    teleop_rotor_count = output["rotor1Engaged"] + output["rotor2Engaged"] + output["rotor3Engaged"] + output["rotor4Engaged"]
     
    output["touchpadNear"]   = robot1sr['climbing']
    output["touchpadMiddle"] = robot2sr['climbing']
    output["touchpadFar"]    = robot3sr['climbing']
    climbing_count = output["touchpadNear"] + output["touchpadMiddle"] + output["touchpadFar"]
     
    output["foulCount"] = robot1sr['foul_percentage'] + robot2sr['foul_percentage'] + robot3sr['foul_percentage']
    output["techFoulCount"] = robot1sr['tech_foul_percentage'] + robot2sr['tech_foul_percentage'] + robot3sr['tech_foul_percentage']
     
    #############
    # Sums
    #############
    kpa_sum = math.floor(auto_fuel_kpa + teleop_fuel_kpa)
    output["autoMobilityPoints"] = mobility_count * 5
    output["autoRotorPoints"] = auto_rotor_count * 60
    output["autoPoints"] = output["autoMobilityPoints"] + output["autoRotorPoints"] + math.floor(auto_fuel_kpa)
     
    output["teleopFuelPoints"] = math.floor(teleop_fuel_kpa)
    output["teleopRotorPoints"] = teleop_rotor_count * 40
    output["teleopTakeoffPoints"] = climbing_count * 50
    output["teleopPoints"] = output["teleopFuelPoints"] + output["teleopRotorPoints"] + output["teleopTakeoffPoints"]
 
    #TODO: Check the points
    output["foulPoints"] = output["foulCount"] * 5 + output["techFoulCount"] * 25
    output["totalPoints"] = output["autoPoints"] + output["teleopPoints"]
 
    output["kPaRankingPointAchieved"] = kpa_sum >= 40
    output["rotorRankingPointAchieved"] = (auto_rotor_count + teleop_rotor_count) == 4
    
    return output


def create_match(official_match_srs, teams):
    
    alliances = []
    
    alliance_color = ["Red", "Blue"]
    
    for i, sr in enumerate(official_match_srs):
        team1sr = teams[sr.team1.teamNumber].create_score_result()
        team2sr = teams[sr.team2.teamNumber].create_score_result()
        team3sr = teams[sr.team3.teamNumber].create_score_result()
        
        alliances.append(populateAlliance(alliance_color[i], team1sr, team2sr, team3sr))
     
    match_scores = collections.OrderedDict()
    match_scores['matchLevel'] = "Qualification"
    match_scores['Alliances'] = alliances
    match_scores['matchNumber'] = str(official_match_srs[0].official_match.matchNumber)
     
    return match_scores


def create_teams(match_nums_to_do):
    
#     from Scouting2017.model import OfficialMatchScoreResult
#     
#     team_numbers = set()
#     
#     for match_num in match_nums_to_do:
#         
#         official_match_srs = OfficialMatchScoreResult.objects.filter(official_match__matchNumber=match_num)
#         
#         for sr in official_match_srs:
#             team_numbers.add(sr.team1.teamNumber)
#             team_numbers.add(sr.team2.teamNumber)
#             team_numbers.add(sr.team3.teamNumber)
#         
#     team_numbers = list(team_numbers)
#     team_numbers = sorted(team_numbers)
#     
#     for team_number in team_numbers:
#         print "    output[%s] = Robot()" % (team_number)

    '''
                     auto_mobility_percentage = 100,
                     auto_gear_percentage = 100,
                     auto_high_goal_percentage = 100,
                     auto_high_goal_capacity = 10,
                     auto_low_goal_percentage = 100,
                     auto_low_goal_capacity = 10,
                     
                     climb_percentage = 100,
                     tele_low_goal_percentage = 100,
                     tele_low_goal_capacity = 150,
                     tele_high_goal_percentage = 100,
                     tele_high_goal_capacity = 120,
                     tele_gear_max = 6,
                     tele_gear_consistancy = 100,
                     
                     foul_percentage=5,
                     tech_foul_percentage=1):
    '''
    

    output = {}    
    output[20] = Robot(auto_high_goal_percentage=90, tele_high_goal_percentage=90, tele_high_goal_capacity=240)
    output[73] = Robot(auto_mobility_percentage=0)
    output[174] = Robot(auto_mobility_percentage=80, tele_gear_max=6, tele_gear_consistancy=90)
    output[191] = Robot(tele_gear_consistancy=80)
    output[250] = Robot()
    output[271] = Robot()
    output[340] = Robot()
    output[378] = Robot()
    output[395] = Robot(tele_gear_max=8, tele_gear_consistancy=60)
    output[578] = Robot()
    output[639] = Robot()
    output[810] = Robot()
    output[1126] = Robot(auto_high_goal_percentage=75, tele_high_goal_percentage=75, tele_high_goal_capacity=160)
    output[1405] = Robot()
    output[1450] = Robot(auto_high_goal_percentage=10, tele_high_goal_percentage=10, tele_high_goal_capacity=40)
    output[1507] = Robot(auto_high_goal_percentage=85, tele_high_goal_percentage=85, tele_high_goal_capacity=200)
    output[1511] = Robot()
    output[1518] = Robot()
    output[1551] = Robot()
    output[1559] = Robot()
    output[1585] = Robot()
    output[1591] = Robot(auto_high_goal_percentage=25, tele_high_goal_percentage=25, tele_high_goal_capacity=90)
    output[1665] = Robot()
    output[1765] = Robot()
    output[1880] = Robot()
    output[2010] = Robot()
    output[2228] = Robot()
    output[2340] = Robot()
    output[2383] = Robot()
    output[2638] = Robot()
    output[2791] = Robot()
    output[2809] = Robot()
    output[3003] = Robot()
    output[3015] = Robot()
    output[3044] = Robot()
    output[3157] = Robot()
    output[3173] = Robot()
    output[3181] = Robot()
    output[3799] = Robot()
    output[3838] = Robot()
    output[3951] = Robot()
    output[4023] = Robot()
    output[4093] = Robot()
    output[4930] = Robot()
    output[5030] = Robot()
    output[5240] = Robot()
    output[5254] = Robot()
    output[5433] = Robot()
    output[5590] = Robot()
    
    return output


def main():
    load_django()
    from Scouting2017.model import OfficialMatch, Match, OfficialMatchScoreResult
    
    random.seed(100)
    
    
    match_nums_to_do = range(1, 40)
    teams = create_teams(match_nums_to_do)
    print teams
    
    
    match_results = {}
     
    matches = []
     
    for match_num in match_nums_to_do:
         
        official_match_srs = OfficialMatchScoreResult.objects.filter(official_match__matchNumber=match_num)
        matches.append(create_match(official_match_srs, teams))
         
 
     
    dump_file = r'C:\Users\PJ\GitHub\SnobotScouting\scouting-app\ScoutingWebsite\Scouting2017\api_scraper_FIRST\api_scraping_results\week3\NYRO_scoreresult_query.json'
     
    match_results['MatchScores'] = matches
    scoreresult_dump = json.dumps(match_results, indent=4)
    with open(dump_file, 'w') as f:
        f.write(scoreresult_dump)

main()