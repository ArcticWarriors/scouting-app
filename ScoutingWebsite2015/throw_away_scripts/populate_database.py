'''
Created on Jan 29, 2016

@author: PJ
'''

#############################################################
# Load django settings so this can be run as a one-off script
#############################################################
import os
import sys
from django.core.wsgi import get_wsgi_application
from pyparsing import srange
import collections

os.environ["DJANGO_SETTINGS_MODULE"] = "ScoutingWebsite.settings"
proj_path = os.path.abspath("..")
sys.path.append(proj_path)
application = get_wsgi_application()

#############################################################

import random
from Scouting2016.model import Team, Match, ScoreResult, OfficialMatch


def __get_create_kargs(present_defense, non_present_defense):

    kargs = {}

    fast_slow_lookup = ['slow', 'fast', 'no_move']
    tower_lookup = ['scale', 'challenge', 'no_points']
    comments_lookup = ["No Comment", "Great robot!", "DO NOT PICK"]
    spybot_lookup = ["yes", "no"]
    auton_defense_cross = ['no_reach', 'reach', 'portcullis', 'cheval', 'moat', 'ramparts', 'bridge', 'sally', 'rock_wall', 'rough', 'low_bar']

    sr_fields = {}

    # Auton
    sr_fields['auto_defense'] = auton_defense_cross[random.randint(0, 10)]
    sr_fields['auto_spy'] = spybot_lookup[random.randint(0, 1)]
    sr_fields['auto_score_low'] = random.randint(0, 1)
    sr_fields['auto_score_high'] = random.randint(0, 1)

    # Boulders
    sr_fields['high_score_fail'] = random.randint(0, 6)
    sr_fields['high_score_successful'] = random.randint(0, 6)
    sr_fields['low_score_fail'] = random.randint(0, 6)
    sr_fields['low_score_successful'] = random.randint(0, 6)

    # Defense Crossing
    for defense in present_defense:
        sr_fields[defense] = random.randint(0, 3)

    for defense in non_present_defense:
        sr_fields[defense] = 0

    # Defense Speed
    sr_fields['slow_fast_portcullis'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_cheval'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_moat'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_ramparts'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_bridge'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_sally'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_rock_wall'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_rough'] = fast_slow_lookup[random.randint(0, 2)]
    sr_fields['slow_fast_low_bar'] = fast_slow_lookup[random.randint(0, 2)]

    # General
    sr_fields['scale_challenge'] = tower_lookup[random.randint(0, 2)]
    sr_fields['score_tech_foul'] = random.randint(0, 2)

    # Comments
    sr_fields['notes_text_area'] = comments_lookup[random.randint(0, 2)]

    for field_name in sr_fields:
        kargs[field_name] = sr_fields[field_name]

    return kargs


def create_teams():

    Team.objects.create(teamNumber=73)
    Team.objects.create(teamNumber=120)
    Team.objects.create(teamNumber=145)
    Team.objects.create(teamNumber=174)
    Team.objects.create(teamNumber=191)
    Team.objects.create(teamNumber=229)
    Team.objects.create(teamNumber=250)
    Team.objects.create(teamNumber=340)
    Team.objects.create(teamNumber=378)
    Team.objects.create(teamNumber=578)
    Team.objects.create(teamNumber=639)
    Team.objects.create(teamNumber=1126)
    Team.objects.create(teamNumber=1405)
    Team.objects.create(teamNumber=1450)
    Team.objects.create(teamNumber=1507)
    Team.objects.create(teamNumber=1511)
    Team.objects.create(teamNumber=1518)
    Team.objects.create(teamNumber=1551)
    Team.objects.create(teamNumber=1559)
    Team.objects.create(teamNumber=1591)
    Team.objects.create(teamNumber=1765)
    Team.objects.create(teamNumber=2053)
    Team.objects.create(teamNumber=2172)
    Team.objects.create(teamNumber=2228)
    Team.objects.create(teamNumber=2340)
    Team.objects.create(teamNumber=3003)
    Team.objects.create(teamNumber=3015)
    Team.objects.create(teamNumber=3044)
    Team.objects.create(teamNumber=3157)
    Team.objects.create(teamNumber=3181)
    Team.objects.create(teamNumber=3613)
    Team.objects.create(teamNumber=3687)
    Team.objects.create(teamNumber=3799)
    Team.objects.create(teamNumber=3838)
    Team.objects.create(teamNumber=3842)
    Team.objects.create(teamNumber=3951)
    Team.objects.create(teamNumber=4093)
    Team.objects.create(teamNumber=4124)
    Team.objects.create(teamNumber=4203)
    Team.objects.create(teamNumber=843)
    Team.objects.create(teamNumber=3173)


def create_matches():

    Match.objects.create(matchNumber=1)
    Match.objects.create(matchNumber=2)
    Match.objects.create(matchNumber=3)
    Match.objects.create(matchNumber=4)
    Match.objects.create(matchNumber=5)
    Match.objects.create(matchNumber=6)
    Match.objects.create(matchNumber=7)
    Match.objects.create(matchNumber=8)
    Match.objects.create(matchNumber=9)
    Match.objects.create(matchNumber=10)
    Match.objects.create(matchNumber=11)
    Match.objects.create(matchNumber=12)
    Match.objects.create(matchNumber=13)
    Match.objects.create(matchNumber=14)
    Match.objects.create(matchNumber=15)
    Match.objects.create(matchNumber=16)
    Match.objects.create(matchNumber=17)
    Match.objects.create(matchNumber=18)
    Match.objects.create(matchNumber=19)
    Match.objects.create(matchNumber=20)
    Match.objects.create(matchNumber=21)
    Match.objects.create(matchNumber=22)
    Match.objects.create(matchNumber=23)
    Match.objects.create(matchNumber=24)
    Match.objects.create(matchNumber=25)
    Match.objects.create(matchNumber=26)
    Match.objects.create(matchNumber=27)
    Match.objects.create(matchNumber=28)
    Match.objects.create(matchNumber=29)
    Match.objects.create(matchNumber=30)
    Match.objects.create(matchNumber=31)
    Match.objects.create(matchNumber=32)
    Match.objects.create(matchNumber=33)
    Match.objects.create(matchNumber=34)
    Match.objects.create(matchNumber=35)
    Match.objects.create(matchNumber=36)
    Match.objects.create(matchNumber=37)
    Match.objects.create(matchNumber=38)
    Match.objects.create(matchNumber=39)
    Match.objects.create(matchNumber=40)


def create_scoreresults():

    teams = Team.objects.all()
    matches = Match.objects.all()

    defenses = collections.OrderedDict()
    defenses['A'] = ('portcullis', 'cheval_de_frise')
    defenses['B'] = ('moat', 'ramparts')
    defenses['C'] = ('draw_bridge', 'sally_port')
    defenses['D'] = ('rock_wall', 'rough_terrain')

    for match in matches:
        team_indices = []
        red_defenses = []
        red_non_defense = []
        blue_defenses = []
        blue_non_defense = []

        for cat in defenses:
            index = random.randint(0, 1)
            red_defenses.append(defenses[cat][index])
            red_non_defense.append(defenses[cat][1 - index])

        for cat in defenses:
            index = random.randint(0, 1)
            blue_defenses.append(defenses[cat][index])
            blue_non_defense.append(defenses[cat][1 - index])

        red_defenses.append('low_bar')
        blue_defenses.append('low_bar')

        while len(team_indices) < 6:
            team_index = random.randint(0, len(teams) - 1)
            if team_index not in team_indices:
                team_indices.append(team_index)

        for i in team_indices:
            team = teams[i]

            if i < 3:
                defense = red_defenses
                non_defense = red_non_defense
            else:
                defense = blue_defenses
                non_defense = blue_non_defense

            kargs = __get_create_kargs(defense, non_defense)
            ScoreResult.objects.create(match=match, team=team, **kargs)


def create_unscouted_matches():

    def create_extra_matches():
        teams = Team.objects.all()
        positions = ['redTeam1', 'redTeam2', 'redTeam3', 'blueTeam1', 'blueTeam2', 'blueTeam3']

    #     for match_number in [21]:
        for match_number in range(41, 80, 1):
            kargs = {}
            kargs['matchNumber'] = match_number

            team_indices = []
            while len(team_indices) < 6:
                team_index = random.randint(0, len(teams) - 1)
                if team_index not in team_indices:
                    team_indices.append(team_index)

            for i in range(len(team_indices)):
                kargs[positions[i]] = teams[team_indices[i]]

            OfficialMatch.objects.create(**kargs)
#             print OfficialMatch(**kargs)

    def create_existing_matches():

        matches = Match.objects.all()

        for match in matches:

            kargs = {}
            kargs['matchNumber'] = match.matchNumber

            positions = ['redTeam1', 'redTeam2', 'redTeam3', 'blueTeam1', 'blueTeam2', 'blueTeam3']
            score_results = score_results = match.scoreresult_set.all()
            for i, sr in enumerate(score_results):
                team = sr.team
                kargs[positions[i]] = team

            OfficialMatch.objects.create(**kargs)
#             print OfficialMatch(**kargs)

    create_existing_matches()
    create_extra_matches()


# create_teams()
# create_matches()
# create_scoreresults()
create_unscouted_matches()
