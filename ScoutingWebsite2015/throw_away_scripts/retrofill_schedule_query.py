'''
Created on Feb 29, 2016

@author: PJ
'''
import os
import sys
import json
import collections
from django.core.wsgi import get_wsgi_application

os.environ["DJANGO_SETTINGS_MODULE"] = "ScoutingWebsite.settings"
proj_path = os.path.abspath("..")
sys.path.append(proj_path)
application = get_wsgi_application()

from Scouting2016.models import OfficialMatch, Match


def dump_schedule():

    schedule = []
    for official_match in OfficialMatch.objects.all():
        match_info = collections.OrderedDict()
        match_info['description'] = "Qualification %s" % official_match.matchNumber
        match_info['field'] = "Primary"
        match_info['matchNumber'] = official_match.matchNumber
        match_info['tournamantLevel'] = "Qualification"

        teams = []
        teams.append({"number": official_match.redTeam1, "station": "Red1", "surrogate": "false"})
        teams.append({"number": official_match.redTeam2, "station": "Red2", "surrogate": "false"})
        teams.append({"number": official_match.redTeam3, "station": "Red3", "surrogate": "false"})
        teams.append({"number": official_match.blueTeam1, "station": "Blue1", "surrogate": "false"})
        teams.append({"number": official_match.blueTeam2, "station": "Blue2", "surrogate": "false"})
        teams.append({"number": official_match.blueTeam3, "station": "Blue3", "surrogate": "false"})

        match_info['Teams'] = teams

        schedule.append(match_info)

    output_file = "__temp_schedule_query.json"
    with open(output_file, 'w') as f:
        json.dump({"Schedule": schedule}, f, indent=4, separators=(',', ': '))


def __get_alliance_sr(color, sr1, sr2, sr3):

    auto_defense_lookup = {}
    auto_defense_lookup['reached'] = "Reached"
    auto_defense_lookup['no_reach'] = "None"

    tower_lookup = {}
    tower_lookup['scale'] = "Both"
    tower_lookup['challenge'] = "Challenged"
    tower_lookup['no_points'] = "None"

    score_results = collections.OrderedDict()
    score_results["alliance"] = color
    score_results["robot1Auto"] = auto_defense_lookup[sr1.auto_defense]
    score_results["robot2Auto"] = auto_defense_lookup[sr2.auto_defense]
    score_results["robot3Auto"] = auto_defense_lookup[sr3.auto_defense]
    score_results["autoBouldersLow"] = sr1.auto_score_low + sr2.auto_score_low + sr3.auto_score_low
    score_results["autoBouldersHigh"] = sr1.auto_score_high + sr2.auto_score_high + sr3.auto_score_high
    score_results["teleopBouldersLow"] = sr1.low_score_successful + sr2.low_score_successful + sr3.low_score_successful
    score_results["teleopBouldersHigh"] = sr1.high_score_successful + sr2.high_score_successful + sr3.high_score_successful
    score_results["towerFaceA"] = tower_lookup[sr1.scale_challenge]
    score_results["towerFaceB"] = tower_lookup[sr2.scale_challenge]
    score_results["towerFaceC"] = tower_lookup[sr3.scale_challenge]
    score_results["towerEndStrength"] = 8 - (score_results["autoBouldersLow"] + score_results["autoBouldersHigh"] + score_results["teleopBouldersLow"] + score_results["teleopBouldersHigh"])
    score_results["teleopTowerCaptured"] = score_results["towerEndStrength"] <= 0 and score_results["towerFaceA"] != "None" and score_results["towerFaceB"] != "None" and score_results["towerFaceC"] != "None"
    score_results["teleopDefensesBreached"] = False
    score_results["position1crossings"] = 2
    score_results["position2"] = "D_RoughTerrain"
    score_results["position2crossings"] = 1
    score_results["position3"] = "A_Portcullis"
    score_results["position3crossings"] = 0
    score_results["position4"] = "C_SallyPort"
    score_results["position4crossings"] = 1
    score_results["position5"] = "B_Moat"
    score_results["position5crossings"] = 1
    score_results["foulCount"] = 0
    score_results["techFoulCount"] = 0
    score_results["autoPoints"] = 0
    score_results["autoReachPoints"] = 0
    score_results["autoCrossingPoints"] = 0
    score_results["autoBoulderPoints"] = 0
    score_results["teleopPoints"] = 0
    score_results["teleopCrossingPoints"] = 0
    score_results["teleopBoulderPoints"] = 0
    score_results["teleopChallengePoints"] = 0
    score_results["teleopScalePoints"] = 0
    score_results["breachPoints"] = 0
    score_results["capturePoints"] = 0
    score_results["adjustPoints"] = 0
    score_results["foulPoints"] = 0
    score_results["totalPoints"] = 0

    return score_results


def dump_match_results():

    match_results = []

    for match in Match.objects.all():

        match_result = collections.OrderedDict()
        match_result["matchLevel"] = "Qualification"
        match_result["matchNumber"] = match.matchNumber
        match_result["AudienceGroup"] = "GroupA"

        score_results = match.scoreresult_set.all()
        if len(score_results) == 6:
            alliances = []
            alliances.append(__get_alliance_sr("Blue", score_results[0], score_results[1], score_results[2]))
            alliances.append(__get_alliance_sr("Red", score_results[3], score_results[4], score_results[5]))
            match_result["Alliances"] = alliances

            match_results.append(match_result)
        else:
            print "OH NOES!"

#         break


#     print json.dumps({"MatchScores": match_results}, indent=4, separators=(',', ': '))
    output_file = "__temp_scoreresult_query.json"
    with open(output_file, 'w') as f:
        json.dump({"MatchScores": match_results}, f, indent=4, separators=(',', ': '))

dump_schedule()
dump_match_results()
