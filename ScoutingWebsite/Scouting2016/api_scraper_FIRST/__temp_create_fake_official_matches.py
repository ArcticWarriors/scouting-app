'''
Created on Feb 7, 2017

@author: PJ
'''
import random
import json
import collections
import math


def getBoolWithPercentage(percentage):
    rando = random.randint(0, 100)
    
    return rando > percentage
    


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



def populateAlliance():
    
    gear_to_rotor_lookup = {}
    gear_to_rotor_lookup[0] = 0
    gear_to_rotor_lookup[1] = 1
    gear_to_rotor_lookup[2] = 1
    gear_to_rotor_lookup[3] = 2
    gear_to_rotor_lookup[4] = 2
    gear_to_rotor_lookup[5] = 2
    gear_to_rotor_lookup[6] = 2
    gear_to_rotor_lookup[7] = 3
    gear_to_rotor_lookup[8] = 3
    gear_to_rotor_lookup[9] = 3
    gear_to_rotor_lookup[10] = 3
    gear_to_rotor_lookup[11] = 3
    gear_to_rotor_lookup[12] = 3
    gear_to_rotor_lookup[13] = 4
    
    auto_gear_percentage = 50
    auto_climb_percentage = 30
    
    output = collections.OrderedDict()

    auto1Gear = 1 if getBoolWithPercentage(auto_gear_percentage) else 0
    auto2Gear = 1 if getBoolWithPercentage(auto_gear_percentage) else 0
    auto3Gear = 1 if getBoolWithPercentage(auto_gear_percentage) else 0
    autoGearSum = auto1Gear + auto2Gear + auto3Gear
    
    # Auto
    output["robot1Auto"] = 'Mobility' if getBoolWithPercentage(50) else 'None'
    output["robot2Auto"] = 'Mobility' if getBoolWithPercentage(50) else 'None'
    output["robot3Auto"] = 'Mobility' if getBoolWithPercentage(50) else 'None'
    output["autoFuelLow"] = 0
    output["autoFuelHigh"] = 0
    output["rotor1Auto"] = 1 if gear_to_rotor_lookup[autoGearSum] >= 1 else 0
    output["rotor2Auto"] = 1 if gear_to_rotor_lookup[autoGearSum] >= 2 else 0
    
    auto_fuel_kpa = output["autoFuelHigh"] + output["autoFuelLow"] / 3.0
    auto_rotor_count = output["rotor1Auto"] + output["rotor2Auto"]
    mobility_count = count_mobility(output["robot1Auto"], output["robot2Auto"], output["robot3Auto"])
    
    
    # Tele
    output["rotor1Engaged"] = (1 if gear_to_rotor_lookup[autoGearSum] >= 1 else 0) - output["rotor1Auto"]
    output["rotor2Engaged"] = (1 if gear_to_rotor_lookup[autoGearSum] >= 2 else 0) - output["rotor2Auto"]
    output["rotor3Engaged"] = (1 if gear_to_rotor_lookup[autoGearSum] >= 3 else 0)
    output["rotor4Engaged"] = (1 if gear_to_rotor_lookup[autoGearSum] >= 4 else 0)
    teleop_rotor_count = output["rotor1Engaged"] + output["rotor2Engaged"] + output["rotor3Engaged"] + output["rotor4Engaged"]
    
    output["teleopFuelLow"] = 0
    output["teleopFuelHigh"] = 0
    teleop_fuel_count = output["teleopFuelLow"] / 3.0 + output["teleopFuelHigh"] / 9.0
    
    output["touchpadNear"] = 1 if getBoolWithPercentage(auto_climb_percentage) else 0
    output["touchpadMiddle"] = 1 if getBoolWithPercentage(auto_climb_percentage) else 0
    output["touchpadFar"] = 1 if getBoolWithPercentage(auto_climb_percentage) else 0
    climbing_count = output["touchpadNear"] + output["touchpadMiddle"] + output["touchpadFar"]
    
    output["foulCount"] = 0
    output["techFoulCount"] = 0
    
    # Sums
    kpa_sum = output["autoFuelLow"] / 3.0 + output["teleopFuelLow"] / 9.0 + output["teleopFuelLow"]  + output["teleopFuelHigh"] / 3.0
    output["autoMobilityPoints"] = mobility_count * 5
    output["autoRotorPoints"] = auto_rotor_count * 60
    output["autoPoints"] = output["autoMobilityPoints"] + output["autoRotorPoints"] + auto_fuel_kpa
    
    output["teleopFuelPoints"] = math.floor(teleop_fuel_count)
    output["teleopRotorPoints"] = teleop_rotor_count * 40
    output["teleopTakeoffPoints"] = climbing_count * 50
    output["teleopPoints"] = output["teleopFuelPoints"] + output["teleopRotorPoints"] + output["teleopTakeoffPoints"]

    #TODO: Check the points
    output["foulPoints"] = output["foulCount"] * 5 + output["techFoulCount"] * 25
    output["totalPoints"] = output["autoPoints"] + output["teleopPoints"]

    output["kPaRankingPointAchieved"] = kpa_sum >= 40
    output["rotorRankingPointAchieved"] = (auto_rotor_count + teleop_rotor_count) == 4
    
    
    
    return output


def create_match(match_number):
    
    
    alliances = []
    
    alliances.append(populateAlliance())
    alliances.append(populateAlliance())
    
#     match_results = {}
    
    match_scores = collections.OrderedDict()
    match_scores['match_level'] = "Qualification"
    match_scores['Alliances'] = alliances
    match_scores['match_number'] = str(match_number)
    
#     match_results['MatchScores'] = match_scores
    
    return match_scores


def main():
    match_nums_to_do = range(1, 40)
    
    random.seed(100)
    
    match_results = {}
    
    matches = []
    
    for match_num in match_nums_to_do:
        matches.append(create_match(match_num))

    
    dump_file = r'C:\Users\PJ\GitHub\SnobotScouting\scouting-app\ScoutingWebsite\Scouting2017\api_scraper_FIRST\api_scraping_results\week3\NYRO_scoreresult_query.json'
    
    match_results['MatchScores'] = matches
    scoreresult_dump = json.dumps(match_results, indent=4)
    with open(dump_file, 'w') as f:
        f.write(scoreresult_dump)

main()