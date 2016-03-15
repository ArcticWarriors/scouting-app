'''
Created on Mar 8, 2016

@author: PJ
'''

import json
from api_scraper import get_users
import sys
import os


def read_local_copy(input_file):
    with open(input_file, 'r') as f:
        response_body = f.read()

    json_struct = json.loads(response_body)

    return json_struct


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


def add_users():
    from django.contrib.auth.models import User, Group

    for user_info in get_users.get_users():
        user_search = User.objects.filter(username=user_info['username'])
        if len(user_search) == 1:
            user = user_search[0]
        else:
            user = User.objects.create_user(username=user_info['username'], password=user_info["password"])

        for group_name in user_info["groups"]:
            group, _ = Group.objects.get_or_create(name=group_name)
            if not user.groups.filter(name=group_name).exists():
                group.user_set.add(user)
                group.save()


if __name__ == "__main__":
    from django.core.wsgi import get_wsgi_application

    event_code = sys.argv[1]
    databse_path = sys.argv[2]
    json_path = sys.argv[3]

    os.environ["DJANGO_SETTINGS_MODULE"] = "ScoutingWebsite.settings"
    proj_path = os.path.abspath("..")
    sys.path.append(proj_path)
    _ = get_wsgi_application()

    print event_code
    print databse_path

    update_schedule(event_code, json_path)
    update_matchresults(event_code, json_path)
    update_team_info(event_code, json_path)
    add_snobot()
    add_users()
