'''
Created on Mar 1, 2016

@author: PJ
'''

#############################################################
# Load django settings so this can be run as a one-off script
#############################################################
import os
import sys
from django.core.wsgi import get_wsgi_application
import random
import collections

os.environ["DJANGO_SETTINGS_MODULE"] = "ScoutingWebsite.settings"
proj_path = os.path.abspath("..")
sys.path.append(proj_path)
application = get_wsgi_application()

#############################################################

from Scouting2016.models import OfficialMatch, ScoreResult, Match


def __populate_sr(auto_low, auto_high, tele_low, tele_high, tech_foul, challenge_string, defense_lookup):

    fast_slow_lookup = ['slow', 'fast', 'no_move']
    comments_lookup = ["No Comment", "Great robot!", "DO NOT PICK"]
    spybot_lookup = ["yes", "no"]
    auton_defense_cross = ['no_reach', 'reach', 'portcullis', 'cheval', 'moat', 'ramparts', 'bridge', 'sally', 'rock_wall', 'rough', 'low_bar']

    sr_fields = collections.OrderedDict()

    sr_fields['auto_score_low'] = auto_low
    sr_fields['auto_score_high'] = auto_high
    sr_fields['high_score_fail'] = 0
    sr_fields['low_score_fail'] = 0
    sr_fields['high_score_successful'] = tele_high
    sr_fields['low_score_successful'] = tele_low
    sr_fields['scale_challenge'] = challenge_string
    sr_fields['score_tech_foul'] = tech_foul

    for category in defense_lookup:
        for defense_name in defense_lookup[category]:
            sr_fields[defense_name] = defense_lookup[category][defense_name]
#
    # Random
    sr_fields['auto_defense'] = auton_defense_cross[random.randint(0, 10)]
    sr_fields['auto_spy'] = spybot_lookup[random.randint(0, 1)]
    sr_fields['slow_fast_portcullis'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_cheval'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_moat'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_ramparts'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_bridge'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_sally'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_rock_wall'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_rough'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_low_bar'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['notes_text_area'] = comments_lookup[random.randint(0, 2)]

    kargs = {}
    for field_name in sr_fields:
        kargs[field_name] = sr_fields[field_name]

    return kargs


def populate_matchresults():

    max_match_number = 50
#     max_match_number = 1

    defenses = collections.OrderedDict()
    defenses['A'] = {'portcullis': 0, 'cheval_de_frise': 0}
    defenses['B'] = {'moat': 0, 'ramparts': 0}
    defenses['C'] = {'draw_bridge': 0, 'sally_port': 0}
    defenses['D'] = {'rock_wall': 0, 'rough_terrain': 0}
    defenses['E'] = {'low_bar': 0}

    for official_match in OfficialMatch.objects.all():
        if official_match.matchNumber > max_match_number:
            continue

        match, _ = Match.objects.get_or_create(matchNumber=official_match.matchNumber)

        red_1_stats = {}
        red_1_stats["auto_low"] = 1 if official_match.redAutoBouldersLow >= 1 else 0
        red_1_stats["auto_high"] = 1 if official_match.redAutoBouldersHigh >= 1 else 0
        red_1_stats["tele_low"] = 1 if official_match.redTeleBouldersLow >= 1 else 0
        red_1_stats["tele_high"] = 1 if official_match.redTeleBouldersHigh >= 1 else 0
        red_1_stats["tech_foul"] = 1 if official_match.redTechFouls >= 1 else 0
        red_1_stats["challenge_string"] = official_match.redTowerFaceA
        red_1_stats["defense_lookup"] = defenses
        sr = ScoreResult(match=match, team=official_match.redTeam1, **__populate_sr(**red_1_stats))
        sr.save()
        print sr

        red_2_stats = {}
        red_2_stats["auto_low"] = 1 if official_match.redAutoBouldersLow >= 2 else 0
        red_2_stats["auto_high"] = 1 if official_match.redAutoBouldersHigh >= 2 else 0
        red_2_stats["tele_low"] = 1 if official_match.redTeleBouldersLow >= 2 else 0
        red_2_stats["tele_high"] = 1 if official_match.redTeleBouldersHigh >= 2 else 0
        red_2_stats["tech_foul"] = 1 if official_match.redTechFouls >= 2 else 0
        red_2_stats["challenge_string"] = official_match.redTowerFaceB
        red_2_stats["defense_lookup"] = defenses
        sr = ScoreResult(match=match, team=official_match.redTeam2, **__populate_sr(**red_2_stats))
        sr.save()

        red_3_stats = {}
        red_3_stats["auto_low"] = official_match.redAutoBouldersLow - 2 if official_match.redAutoBouldersLow >= 3 else 0
        red_3_stats["auto_high"] = official_match.redAutoBouldersHigh - 2 if official_match.redAutoBouldersHigh >= 3 else 0
        red_3_stats["tele_low"] = official_match.redTeleBouldersLow - 2 if official_match.redTeleBouldersLow >= 3 else 0
        red_3_stats["tele_high"] = official_match.redTeleBouldersHigh - 2 if official_match.redTeleBouldersHigh >= 3 else 0
        red_3_stats["tech_foul"] = official_match.redTechFouls - 2 if official_match.redTechFouls >= 3 else 0
        red_3_stats["challenge_string"] = official_match.redTowerFaceC
        red_3_stats["defense_lookup"] = defenses
        sr = ScoreResult(match=match, team=official_match.redTeam3, **__populate_sr(**red_3_stats))
        sr.save()

        blue_1_stats = {}
        blue_1_stats["auto_low"] = 1 if official_match.blueAutoBouldersLow >= 1 else 0
        blue_1_stats["auto_high"] = 1 if official_match.blueAutoBouldersHigh >= 1 else 0
        blue_1_stats["tele_low"] = 1 if official_match.blueTeleBouldersLow >= 1 else 0
        blue_1_stats["tele_high"] = 1 if official_match.blueTeleBouldersHigh >= 1 else 0
        blue_1_stats["tech_foul"] = 1 if official_match.blueTechFouls >= 1 else 0
        blue_1_stats["challenge_string"] = official_match.blueTowerFaceA
        blue_1_stats["defense_lookup"] = defenses
        sr = ScoreResult(match=match, team=official_match.blueTeam1, **__populate_sr(**blue_1_stats))
        sr.save()

        blue_2_stats = {}
        blue_2_stats["auto_low"] = 1 if official_match.blueAutoBouldersLow >= 2 else 0
        blue_2_stats["auto_high"] = 1 if official_match.blueAutoBouldersHigh >= 2 else 0
        blue_2_stats["tele_low"] = 1 if official_match.blueTeleBouldersLow >= 2 else 0
        blue_2_stats["tele_high"] = 1 if official_match.blueTeleBouldersHigh >= 2 else 0
        blue_2_stats["tech_foul"] = 1 if official_match.blueTechFouls >= 2 else 0
        blue_2_stats["challenge_string"] = official_match.blueTowerFaceB
        blue_2_stats["defense_lookup"] = defenses
        sr = ScoreResult(match=match, team=official_match.blueTeam2, **__populate_sr(**blue_2_stats))
        sr.save()

        blue_3_stats = {}
        blue_3_stats["auto_low"] = official_match.blueAutoBouldersLow - 2 if official_match.blueAutoBouldersLow >= 3 else 0
        blue_3_stats["auto_high"] = official_match.blueAutoBouldersHigh - 2 if official_match.blueAutoBouldersHigh >= 3 else 0
        blue_3_stats["tele_low"] = official_match.blueTeleBouldersLow - 2 if official_match.blueTeleBouldersLow >= 3 else 0
        blue_3_stats["tele_high"] = official_match.blueTeleBouldersHigh - 2 if official_match.blueTeleBouldersHigh >= 3 else 0
        blue_3_stats["tech_foul"] = official_match.blueTechFouls - 2 if official_match.blueTechFouls >= 3 else 0
        blue_3_stats["challenge_string"] = official_match.blueTowerFaceC
        blue_3_stats["defense_lookup"] = defenses
        sr = ScoreResult(match=match, team=official_match.blueTeam3, **__populate_sr(**blue_3_stats))
        sr.save()

        print
        print


    pass


populate_matchresults()
