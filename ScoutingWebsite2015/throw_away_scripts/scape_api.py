'''
Created on Feb 28, 2016

@author: PJ
'''

#############################################################
# Load django settings so this can be run as a one-off script
#############################################################
import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ["DJANGO_SETTINGS_MODULE"] = "ScoutingWebsite.settings"
proj_path = os.path.abspath("..")
sys.path.append(proj_path)
application = get_wsgi_application()

#############################################################


import json
from urllib2 import Request, urlopen
from Scouting2016.models import OfficialMatch


def scrape_schedule(event_code, start):
    tourny_level = "Qualification"

    url = "https://private-anon-92454c480-frcevents2.apiary-mock.com/v2.0/2016/schedule/{0}?tournamentLevel={1}&start={2}".format(event_code, tourny_level, start)

    headers = {'Accept': 'application/json'}
    request = Request(url, headers=headers)

    # response_body = urlopen(request).read()
    with open('__temp_schedule_query.json', 'r') as f:
        response_body = f.read()

    schedule_info = json.loads(response_body)["Schedule"]

    # print response_body

    for match_info in schedule_info:
        match_number = match_info["matchNumber"]
        teams = []
        for team_info in match_info["Teams"]:
            teams.append(team_info["number"])
        print match_number, teams


def scrape_match_results(event_code, start):
    tourny_level = "Qualification"
    season = "2016"

    url = "https://private-anon-92454c480-frcevents2.apiary-mock.com/v2.0/{0}/scores/{1}/{2}?start={3}".format(season, event_code, tourny_level, start)

    headers = {'Accept': 'application/json'}
    request = Request(url, headers=headers)

#     response_body = urlopen(request).read()
#     print response_body
    with open('__temp_scoreresult_query.json', 'r') as f:
        response_body = f.read()

    scores_info = json.loads(response_body)["MatchScores"]
    for match_info in scores_info:
        match_number = match_info["matchNumber"]

        official_match = OfficialMatch.objects.get(matchNumber=match_number)

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
            else:
                print "OH NOES!"

        official_match.save()


event_code = "NYROC"
match_start = 0

# scrape_schedule(event_code, match_start)
scrape_match_results(event_code, match_start)
