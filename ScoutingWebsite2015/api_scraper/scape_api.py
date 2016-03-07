'''
Created on Feb 28, 2016

@author: PJ
'''
import subprocess
import os


#############################################################
# Load django settings so this can be run as a one-off script
#############################################################
def reload_django(event_code, database_path):
    import os
    import sys

    with open('../ScoutingWebsite/database_path.py', 'w') as f:
        f.write("database_path = '" + database_path + "/%s.sqlite3'" % event_code)
    cur_dir = os.getcwd()
    os.chdir("..")
    subprocess.call(["python", "manage.py", "migrate"])
    os.chdir(cur_dir)

    from django.core.wsgi import get_wsgi_application

    os.environ["DJANGO_SETTINGS_MODULE"] = "ScoutingWebsite.settings"
    proj_path = os.path.abspath("..")
    sys.path.append(proj_path)
    _ = get_wsgi_application()

#############################################################

import json
from urllib2 import Request, urlopen

from api_scraper.api_key import get_encoded_key


__api_website = "https://frc-api.firstinspires.org/v2.0/"


def get_header():

    headers = {}
    headers['Accept'] = 'application/json'
    headers['Authorization'] = 'Basic ' + get_encoded_key()

    return headers


def read_url_and_dump(url, headers, output_file):
    request = Request(url, headers=headers)
    response_body = urlopen(request).read()

    json_struct = json.loads(response_body)

    with open(output_file, 'w') as f:
        json.dump(json_struct, f, indent=4, separators=(',', ': '))

    return json_struct


def read_local_copy(input_file):
    with open(input_file, 'r') as f:
        response_body = f.read()

    json_struct = json.loads(response_body)

    return json_struct


def download_team_info(event_code, json_path, season="2016"):

    url = __api_website + "/{0}/teams?eventCode={1}".format(season, event_code)
    local_file = json_path + '/{0}_team_query.json'.format(event_code)
    read_url_and_dump(url, get_header(), local_file)


def download_matchresult_info(event_code, start, json_path, season="2016", tourny_level="Qualification"):
    url = __api_website + "/{0}/scores/{1}/{2}?start={3}".format(season, event_code, tourny_level, start)
    local_file = json_path + '/{0}_scoreresult_query.json'.format(event_code)
    read_url_and_dump(url, get_header(), local_file)


def download_schedule(event_code, start, json_path, season="2016", tourny_level="Qualification"):
    url = __api_website + "/{0}/schedule/{1}?tournamentLevel={2}&start={3}".format(season, event_code, tourny_level, start)
    local_file = json_path + '/{0}_schedule_query.json'.format(event_code)
    read_url_and_dump(url, get_header(), local_file)


def update_team_info(event_code, json_path):
    from Scouting2016.models import Team

    local_file = json_path + '/{0}_team_query.json'.format(event_code)
    json_struct = read_local_copy(local_file)

    for team_info in json_struct["teams"]:
        team_number = team_info["teamNumber"]

        team = Team.objects.get(teamNumber=team_number)
        team.homepage = team_info["website"] if team_info["website"] != None else "NA"
        team.teamFirstYear = team_info["rookieYear"]
        team.save()
        print "Updating info for team %s" % team_number


def update_schedule(event_code, json_path):
    from Scouting2016.models import OfficialMatch, Team

    local_file = json_path + '/{0}_schedule_query.json'.format(event_code)
    json_struct = read_local_copy(local_file)

    schedule_info = json_struct["Schedule"]

    for match_info in schedule_info:
        match_number = match_info["matchNumber"]

        red_teams = []
        blue_teams = []

        for team_info in match_info["Teams"]:
            team, _ = Team.objects.get_or_create(teamNumber=team_info["teamNumber"])
            if "Red" in team_info["station"]:
                red_teams.append(team)
            else:
                blue_teams.append(team)

        official_search = OfficialMatch.objects.filter(matchNumber=match_number)
        if len(official_search) == 0:
            official_match = OfficialMatch.objects.create(matchNumber=match_number,
                                                          redTeam1=red_teams[0],
                                                          redTeam2=red_teams[1],
                                                          redTeam3=red_teams[2],
                                                          blueTeam1=blue_teams[0],
                                                          blueTeam2=blue_teams[1],
                                                          blueTeam3=blue_teams[2])
        else:
            official_match = official_search[0]
            official_match.redTeam1 = red_teams[0]
            official_match.redTeam2 = red_teams[1]
            official_match.redTeam3 = red_teams[2]
            official_match.blueTeam1 = blue_teams[0]
            official_match.blueTeam2 = blue_teams[1]
            official_match.blueTeam3 = blue_teams[2]
            official_match.save()

        print "Creating scheduled match %s with red team=%s, blue teams=%s" % (match_number, red_teams, blue_teams)


def update_matchresults(event_code, json_path):
    from Scouting2016.models import OfficialMatch

    local_file = json_path + '/{0}_scoreresult_query.json'.format(event_code)
    json_struct = read_local_copy(local_file)

    defense_name_lookup = {}
    defense_name_lookup["A_Portcullis"] = "portcullis"
    defense_name_lookup["A_ChevalDeFrise"] = "cheval_de_frise"
    defense_name_lookup["B_Moat"] = "moat"
    defense_name_lookup["B_Ramparts"] = "ramparts"
    defense_name_lookup["C_Drawbridge"] = "draw_bridge"
    defense_name_lookup["C_SallyPort"] = "sally_port"
    defense_name_lookup["D_RockWall"] = "rock_wall"
    defense_name_lookup["D_RoughTerrain"] = "rough_terrain"
    defense_name_lookup["NotSpecified"] = "NA"

    scores_info = json_struct["MatchScores"]
    for match_info in scores_info:
        match_number = match_info["matchNumber"]
        audience_defense = match_info["AudienceGroup"][-1]

        official_match = OfficialMatch.objects.get(matchNumber=match_number)
        official_match.audienceSelectionCategory = audience_defense

        for alliance_info in match_info["Alliances"]:
            color = alliance_info["alliance"]
            if color == "Red":
                official_match.redAutoBouldersLow = alliance_info["autoBouldersLow"]
                official_match.redAutoBouldersHigh = alliance_info["autoBouldersHigh"]
                official_match.redTeleBouldersLow = alliance_info["teleopBouldersLow"]
                official_match.redTeleBouldersHigh = alliance_info["teleopBouldersHigh"]
                official_match.redTowerFaceA = alliance_info["towerFaceA"]
                official_match.redTowerFaceB = alliance_info["towerFaceB"]
                official_match.redTowerFaceC = alliance_info["towerFaceC"]
                official_match.redFouls = alliance_info["foulCount"]
                official_match.redTechFouls = alliance_info["techFoulCount"]

                official_match.redDefense2Name = defense_name_lookup[alliance_info["position2"]]
                official_match.redDefense3Name = defense_name_lookup[alliance_info["position3"]]
                official_match.redDefense4Name = defense_name_lookup[alliance_info["position4"]]
                official_match.redDefense5Name = defense_name_lookup[alliance_info["position5"]]
                official_match.redDefense1Crossings = alliance_info["position1crossings"]
                official_match.redDefense2Crossings = alliance_info["position2crossings"]
                official_match.redDefense3Crossings = alliance_info["position3crossings"]
                official_match.redDefense4Crossings = alliance_info["position4crossings"]
                official_match.redDefense5Crossings = alliance_info["position5crossings"]

            elif color == "Blue":
                official_match.blueAutoBouldersLow = alliance_info["autoBouldersLow"]
                official_match.blueAutoBouldersHigh = alliance_info["autoBouldersHigh"]
                official_match.blueTeleBouldersLow = alliance_info["teleopBouldersLow"]
                official_match.blueTeleBouldersHigh = alliance_info["teleopBouldersHigh"]
                official_match.blueTowerFaceA = alliance_info["towerFaceA"]
                official_match.blueTowerFaceB = alliance_info["towerFaceB"]
                official_match.blueTowerFaceC = alliance_info["towerFaceC"]
                official_match.blueFouls = alliance_info["foulCount"]
                official_match.blueTechFouls = alliance_info["techFoulCount"]

                official_match.blueDefense2Name = defense_name_lookup[alliance_info["position2"]]
                official_match.blueDefense3Name = defense_name_lookup[alliance_info["position3"]]
                official_match.blueDefense4Name = defense_name_lookup[alliance_info["position4"]]
                official_match.blueDefense5Name = defense_name_lookup[alliance_info["position5"]]
                official_match.blueDefense1Crossings = alliance_info["position1crossings"]
                official_match.blueDefense2Crossings = alliance_info["position2crossings"]
                official_match.blueDefense3Crossings = alliance_info["position3crossings"]
                official_match.blueDefense4Crossings = alliance_info["position4crossings"]
                official_match.blueDefense5Crossings = alliance_info["position5crossings"]
            else:
                print "OH NOES!"

        official_match.save()
        print "Adding stats to official match %s" % official_match.matchNumber


def add_snobot():
    from Scouting2016.models import Team
    query = Team.objects.filter(teamNumber=174)
    if len(query) == 0:
        team = Team.objects.all()[0]
        team.teamNumber = 174
        team.save()
        print "Adding 174 to regional"


# Week 1
event_codes = []
event_codes.append("ONTO2")
event_codes.append("ISTA")
event_codes.append("MNDU")
event_codes.append("MNDU2")
event_codes.append("SCMB")
event_codes.append("CASD")
event_codes.append("VAHAY")
event_codes.append("MIKET")
event_codes.append("MISOU")
event_codes.append("MISTA")
event_codes.append("MIWAT")
event_codes.append("PAHAT")
event_codes.append("NJFLA")
event_codes.append("NCMCL")
event_codes.append("NHGRS")
event_codes.append("CTWAT")
event_codes.append("WAAMV")
event_codes.append("WASPO")

match_start = 0
download_results = True
update_database = False
sql_path = "__api_scraping_results/database/week1"
json_path = "../__api_scraping_results/json/week1"

for ec in event_codes:
    if download_results:
        print "Downloading results for regional %s" % ec
        download_matchresult_info(ec, match_start, json_path)
        download_schedule(ec, match_start, json_path)
        download_team_info(ec, json_path)

    if update_database:
        update_schedule(ec, json_path)
        update_matchresults(ec, json_path)
        update_team_info(ec, json_path)
        add_snobot()
