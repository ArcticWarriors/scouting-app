'''
Created on Feb 28, 2016

@author: PJ
'''
import json
from urllib2 import Request, urlopen


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
        print match_number,

        for alliance_info in match_info["Alliances"]:
            color = alliance_info["alliance"]
            print color, alliance_info["position1crossings"],

        print


event_code = "NYROC"
match_start = 0

# scrape_schedule(event_code, match_start)
scrape_match_results(event_code, match_start)
