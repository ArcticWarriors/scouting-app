'''
Created on Mar 1, 2016

@author: PJ
'''
import collections
import random
import sys
import os
import subprocess
from api_scraper.get_competitions import get_competitions_to_scrape


#############################################################
# Load django settings so this can be run as a one-off script
#############################################################

def reload_django(event_code, database_path):

    from django.core.wsgi import get_wsgi_application

    with open('../ScoutingWebsite/database_path.py', 'w') as f:
        f.write("database_path = '" + database_path + "/%s.sqlite3'" % event_code)

    os.environ["DJANGO_SETTINGS_MODULE"] = "ScoutingWebsite.settings"
    proj_path = os.path.abspath("..")
    sys.path.append(proj_path)
    _ = get_wsgi_application()


def __populate_sr(auto_cross, auto_low, auto_high, tele_low, tele_high, tech_foul, challenge_string, defense_lookup, defense_speed_lookup):

    comments_lookup = ["No Comment", "Great robot!", "DO NOT PICK"]
    spybot_lookup = ["yes", "no"]
    auton_defense_cross = ['portcullis', 'cheval', 'moat', 'ramparts', 'bridge', 'sally', 'rock_wall', 'rough', 'low_bar']

    sr_fields = collections.OrderedDict()

    sr_fields['auto_score_low'] = auto_low
    sr_fields['auto_score_high'] = auto_high
    sr_fields['high_score_fail'] = 0
    sr_fields['low_score_fail'] = 0
    sr_fields['high_score_successful'] = tele_high
    sr_fields['low_score_successful'] = tele_low
    sr_fields['scale_challenge'] = challenge_string
    sr_fields['score_tech_foul'] = tech_foul
         
    if auto_cross == "None":
        sr_fields['auto_defense'] = "no_reach"
    elif auto_cross == "Reached":
        sr_fields['auto_defense'] = "reach"
    else:
        sr_fields['auto_defense'] = auton_defense_cross[random.randint(0, 8)]

    for defense in defense_lookup:
        sr_fields[defense] = defense_lookup[defense]

    for defense in defense_speed_lookup:
        sr_fields[defense] = defense_speed_lookup[defense]
#
    # Random
    sr_fields['auto_spy'] = spybot_lookup[random.randint(0, 1)]
    sr_fields['notes_text_area'] = comments_lookup[random.randint(0, 2)]

    kargs = {}
    for field_name in sr_fields:
        kargs[field_name] = sr_fields[field_name]

    return kargs


def __populate_defense(official_match, color, team_index):

    fast_slow_lookup = ['slow', 'fast']

    defenses = collections.OrderedDict()
    defenses['portcullis'] = 0
    defenses['cheval_de_frise'] = 0
    defenses['moat'] = 0
    defenses['ramparts'] = 0
    defenses['draw_bridge'] = 0
    defenses['sally_port'] = 0
    defenses['rock_wall'] = 0
    defenses['rough_terrain'] = 0
    defenses['low_bar'] = 0

    defenses_speed = collections.OrderedDict()
    defenses_speed['slow_fast_portcullis'] = 'no_move'
    defenses_speed['slow_fast_cheval_de_frise'] = 'no_move'
    defenses_speed['slow_fast_moat'] = 'no_move'
    defenses_speed['slow_fast_ramparts'] = 'no_move'
    defenses_speed['slow_fast_draw_bridge'] = 'no_move'
    defenses_speed['slow_fast_sally_port'] = 'no_move'
    defenses_speed['slow_fast_rock_wall'] = 'no_move'
    defenses_speed['slow_fast_rough_terrain'] = 'no_move'
    defenses_speed['slow_fast_low_bar'] = 'no_move'

    if color == "red":
        defense1Name = 'low_bar'
        defense2Name = official_match.redDefense2Name
        defense3Name = official_match.redDefense3Name
        defense4Name = official_match.redDefense4Name
        defense5Name = official_match.redDefense5Name

        if defense1Name != "NA" and official_match.redDefense1Crossings > team_index:
            defenses[defense1Name] = 1
            defenses_speed['slow_fast_' + defense1Name] = fast_slow_lookup[random.randint(0, 1)]
            

        if defense2Name != "NA" and official_match.redDefense2Crossings > team_index:
            defenses[defense2Name] = 1
            defenses_speed['slow_fast_' + defense2Name] = fast_slow_lookup[random.randint(0, 1)]

        if defense3Name != "NA" and official_match.redDefense3Crossings > team_index:
            defenses[defense3Name] = 1
            defenses_speed['slow_fast_' + defense3Name] = fast_slow_lookup[random.randint(0, 1)]

        if defense4Name != "NA" and official_match.redDefense4Crossings > team_index:
            defenses[defense4Name] = 1
            defenses_speed['slow_fast_' + defense4Name] = fast_slow_lookup[random.randint(0, 1)]

        if defense5Name != "NA" and official_match.redDefense5Crossings > team_index:
            defenses[defense5Name] = 1
            defenses_speed['slow_fast_' + defense5Name] = fast_slow_lookup[random.randint(0, 1)]

    if color == "blue":
        defense1Name = 'low_bar'
        defense2Name = official_match.blueDefense2Name
        defense3Name = official_match.blueDefense3Name
        defense4Name = official_match.blueDefense4Name
        defense5Name = official_match.blueDefense5Name

        if defense1Name != "NA" and official_match.blueDefense1Crossings > team_index:
            defenses[defense1Name] = 1
            defenses_speed['slow_fast_' + defense1Name] = fast_slow_lookup[random.randint(0, 1)]

        if defense2Name != "NA" and official_match.blueDefense2Crossings > team_index:
            defenses[defense2Name] = 1
            defenses_speed['slow_fast_' + defense2Name] = fast_slow_lookup[random.randint(0, 1)]

        if defense3Name != "NA" and official_match.blueDefense3Crossings > team_index:
            defenses[defense3Name] = 1
            defenses_speed['slow_fast_' + defense3Name] = fast_slow_lookup[random.randint(0, 1)]

        if defense4Name != "NA" and official_match.blueDefense4Crossings > team_index:
            defenses[defense4Name] = 1
            defenses_speed['slow_fast_' + defense4Name] = fast_slow_lookup[random.randint(0, 1)]

        if defense5Name != "NA" and official_match.blueDefense5Crossings > team_index:
            defenses[defense5Name] = 1
            defenses_speed['slow_fast_' + defense5Name] = fast_slow_lookup[random.randint(0, 1)]

    return defenses, defenses_speed


def __save_sr(match, team, **kargs):

    from Scouting2016.models import ScoreResult

    sr_search = ScoreResult.objects.filter(match=match, team=team)
    if len(sr_search) == 0:
        sr = ScoreResult(match=match, team=team, **kargs)
        sr.save()
        pass
    else:
        sr = sr_search[0]
        for key, value in kargs.iteritems():
            setattr(sr, key, value)
        sr.save()
#         print sr
        pass


def populate_matchresults(max_match_number, max_match_with_data_number):

    from Scouting2016.models import OfficialMatch, Match

    for official_match in OfficialMatch.objects.all():
        if official_match.matchNumber > max_match_number:
            continue

        match, _ = Match.objects.get_or_create(matchNumber=official_match.matchNumber)
        print "Updating match %s" % match.matchNumber

        red_1_stats = {}
        defense_crossings, defense_speed = __populate_defense(official_match, "red", 0)
        red_1_stats["auto_cross"] = official_match.redAutonA
        red_1_stats["auto_low"] = 1 if official_match.redAutoBouldersLow >= 1 else 0
        red_1_stats["auto_high"] = 1 if official_match.redAutoBouldersHigh >= 1 else 0
        red_1_stats["tele_low"] = 1 if official_match.redTeleBouldersLow >= 1 else 0
        red_1_stats["tele_high"] = 1 if official_match.redTeleBouldersHigh >= 1 else 0
        red_1_stats["tech_foul"] = 1 if official_match.redTechFouls >= 1 else 0
        red_1_stats["challenge_string"] = official_match.redTowerFaceA
        red_1_stats["defense_lookup"] = defense_crossings
        red_1_stats["defense_speed_lookup"] = defense_speed
        __save_sr(match=match, team=official_match.redTeam1, **__populate_sr(**red_1_stats))

        red_2_stats = {}
        defense_crossings, defense_speed = __populate_defense(official_match, "red", 1)
        red_2_stats["auto_cross"] = official_match.redAutonB
        red_2_stats["auto_low"] = 1 if official_match.redAutoBouldersLow >= 2 else 0
        red_2_stats["auto_high"] = 1 if official_match.redAutoBouldersHigh >= 2 else 0
        red_2_stats["tele_low"] = 1 if official_match.redTeleBouldersLow >= 2 else 0
        red_2_stats["tele_high"] = 1 if official_match.redTeleBouldersHigh >= 2 else 0
        red_2_stats["tech_foul"] = 1 if official_match.redTechFouls >= 2 else 0
        red_2_stats["challenge_string"] = official_match.redTowerFaceB
        red_2_stats["defense_lookup"] = defense_crossings
        red_2_stats["defense_speed_lookup"] = defense_speed
        __save_sr(match=match, team=official_match.redTeam2, **__populate_sr(**red_2_stats))

        red_3_stats = {}
        defense_crossings, defense_speed = __populate_defense(official_match, "red", 3)
        red_3_stats["auto_cross"] = official_match.redAutonC
        red_3_stats["auto_low"] = official_match.redAutoBouldersLow - 2 if official_match.redAutoBouldersLow >= 3 else 0
        red_3_stats["auto_high"] = official_match.redAutoBouldersHigh - 2 if official_match.redAutoBouldersHigh >= 3 else 0
        red_3_stats["tele_low"] = official_match.redTeleBouldersLow - 2 if official_match.redTeleBouldersLow >= 3 else 0
        red_3_stats["tele_high"] = official_match.redTeleBouldersHigh - 2 if official_match.redTeleBouldersHigh >= 3 else 0
        red_3_stats["tech_foul"] = official_match.redTechFouls - 2 if official_match.redTechFouls >= 3 else 0
        red_3_stats["challenge_string"] = official_match.redTowerFaceC
        red_3_stats["defense_lookup"] = defense_crossings
        red_3_stats["defense_speed_lookup"] = defense_speed
        __save_sr(match=match, team=official_match.redTeam3, **__populate_sr(**red_3_stats))

        blue_1_stats = {}
        defense_crossings, defense_speed = __populate_defense(official_match, "blue", 0)
        blue_1_stats["auto_cross"] = official_match.blueAutonA
        blue_1_stats["auto_low"] = 1 if official_match.blueAutoBouldersLow >= 1 else 0
        blue_1_stats["auto_high"] = 1 if official_match.blueAutoBouldersHigh >= 1 else 0
        blue_1_stats["tele_low"] = 1 if official_match.blueTeleBouldersLow >= 1 else 0
        blue_1_stats["tele_high"] = 1 if official_match.blueTeleBouldersHigh >= 1 else 0
        blue_1_stats["tech_foul"] = 1 if official_match.blueTechFouls >= 1 else 0
        blue_1_stats["challenge_string"] = official_match.blueTowerFaceA
        blue_1_stats["defense_lookup"] = defense_crossings
        blue_1_stats["defense_speed_lookup"] = defense_speed
        __save_sr(match=match, team=official_match.blueTeam1, **__populate_sr(**blue_1_stats))

        blue_2_stats = {}
        defense_crossings, defense_speed = __populate_defense(official_match, "blue", 1)
        blue_2_stats["auto_cross"] = official_match.blueAutonB
        blue_2_stats["auto_low"] = 1 if official_match.blueAutoBouldersLow >= 2 else 0
        blue_2_stats["auto_high"] = 1 if official_match.blueAutoBouldersHigh >= 2 else 0
        blue_2_stats["tele_low"] = 1 if official_match.blueTeleBouldersLow >= 2 else 0
        blue_2_stats["tele_high"] = 1 if official_match.blueTeleBouldersHigh >= 2 else 0
        blue_2_stats["tech_foul"] = 1 if official_match.blueTechFouls >= 2 else 0
        blue_2_stats["challenge_string"] = official_match.blueTowerFaceB
        blue_2_stats["defense_lookup"] = defense_crossings
        blue_2_stats["defense_speed_lookup"] = defense_speed
        __save_sr(match=match, team=official_match.blueTeam2, **__populate_sr(**blue_2_stats))

        blue_3_stats = {}
        defense_crossings, defense_speed = __populate_defense(official_match, "blue", 2)
        blue_3_stats["auto_cross"] = official_match.blueAutonC
        blue_3_stats["auto_low"] = official_match.blueAutoBouldersLow - 2 if official_match.blueAutoBouldersLow >= 3 else 0
        blue_3_stats["auto_high"] = official_match.blueAutoBouldersHigh - 2 if official_match.blueAutoBouldersHigh >= 3 else 0
        blue_3_stats["tele_low"] = official_match.blueTeleBouldersLow - 2 if official_match.blueTeleBouldersLow >= 3 else 0
        blue_3_stats["tele_high"] = official_match.blueTeleBouldersHigh - 2 if official_match.blueTeleBouldersHigh >= 3 else 0
        blue_3_stats["tech_foul"] = official_match.blueTechFouls - 2 if official_match.blueTechFouls >= 3 else 0
        blue_3_stats["challenge_string"] = official_match.blueTowerFaceC
        blue_3_stats["defense_lookup"] = defense_crossings
        blue_3_stats["defense_speed_lookup"] = defense_speed
        __save_sr(match=match, team=official_match.blueTeam3, **__populate_sr(**blue_3_stats))

        official_match.hasOfficialData = True
        official_match.save()


if len(sys.argv) <= 1:
    for json_path, sql_path, ec in get_competitions_to_scrape():
        reload_django(ec, sql_path)
        subprocess.call(['python', sys.argv[0], ec, sql_path, "50", "45"])
else:
    from django.core.wsgi import get_wsgi_application

    event_code = sys.argv[1]
    databse_path = sys.argv[2]
    max_match_number = int(sys.argv[3])
    max_match_with_data_number = int(sys.argv[4])
#     json_path = sys.argv[3]

    os.environ["DJANGO_SETTINGS_MODULE"] = "ScoutingWebsite.settings"
    proj_path = os.path.abspath("..")
    sys.path.append(proj_path)
    _ = get_wsgi_application()

    reload_django(event_code, databse_path)
    populate_matchresults(max_match_number, max_match_with_data_number)
