'''
Created on Mar 1, 2017

@author: PJ
'''
import collections


def get_teams_sr(alliance_color, match, team1, team2, team3, official_sr):


    team1sr = None
    team2sr = None
    team3sr = None

    # TODO: there has to be a better way... but I'd rather not touch the DB
    for sr in team1.scoreresult_set.all():
        if sr.match.matchNumber == official_sr.official_match.matchNumber:
            team1sr = sr
            break

    for sr in team2.scoreresult_set.all():
        if sr.match.matchNumber == official_sr.official_match.matchNumber:
            team2sr = sr
            break

    for sr in team3.scoreresult_set.all():
        if sr.match.matchNumber == official_sr.official_match.matchNumber:
            team3sr = sr
            break

    team_srs = [team1sr, team2sr, team3sr]
    team_srs = [sr for sr in team_srs if sr != None]

    teams_scouted = set([sr.team for sr in team_srs])

    if alliance_color == "Red":
        teams_required = set([match.red1, match.red2, match.red3])
    elif alliance_color == "Blue":
        teams_required = set([match.blue1, match.blue2, match.blue3])

    missing_teams = teams_required.difference(teams_scouted)

    return team_srs, missing_teams


def validate_alliance_score(alliance_color, team_srs, official_sr):

    warning_messages = []
    error_messages = []

    auto_fuel_low_sum = 0
    auto_fuel_high_sum = 0
    tele_fuel_low_sum = 0
    tele_fuel_high_sum = 0

    auto_gear_sum = 0
    tele_gear_sum = 0

    climb_sum = 0
    basline_sum = 0

    for sr in team_srs:
        auto_fuel_low_sum += sr.auto_fuel_low_score
        auto_fuel_high_sum += sr.auto_fuel_high_score
        tele_fuel_low_sum += sr.tele_fuel_low_score
        tele_fuel_high_sum += sr.tele_fuel_high_score

        auto_gear_sum += sr.auto_gears
        tele_gear_sum += sr.tele_gears

        climb_sum += 1 if sr.rope else 0
        basline_sum += 1 if sr.auto_baseline else 0

    ######################
    # Fuel
    ######################
    if official_sr.autoFuelLow != auto_fuel_low_sum:
        warning_messages.append((alliance_color + "Auto Low Fuel", official_sr.autoFuelLow, auto_fuel_low_sum))

    if official_sr.autoFuelHigh != auto_fuel_high_sum:
        warning_messages.append((alliance_color + "Auto High Fuel", official_sr.autoFuelHigh, auto_fuel_high_sum))

    if official_sr.teleopFuelLow != tele_fuel_low_sum:
        warning_messages.append((alliance_color + "Tele Low Fuel", official_sr.teleopFuelLow, tele_fuel_low_sum))

    if official_sr.teleopFuelHigh != tele_fuel_high_sum:
        warning_messages.append((alliance_color + "Tele High Fuel", official_sr.teleopFuelHigh, tele_fuel_high_sum))

    #######################
    # Gears
    #######################
    actual_auto_rotor1 = official_sr.rotor1Auto == 1
    actual_auto_rotor2 = official_sr.rotor2Auto == 1
    actual_tele_rotor1 = official_sr.rotor1Engaged == 1
    actual_tele_rotor2 = official_sr.rotor2Engaged == 1
    actual_tele_rotor3 = official_sr.rotor3Engaged == 1
    actual_tele_rotor4 = official_sr.rotor4Engaged == 1

    expected_auto_rotor1 = auto_gear_sum >= 1
    expected_auto_rotor2 = auto_gear_sum >= 3
    expected_tele_rotor1 = tele_gear_sum >= 1 and not expected_auto_rotor1
    expected_tele_rotor2 = tele_gear_sum >= 3 and not expected_auto_rotor2
    expected_tele_rotor3 = tele_gear_sum >= 7
    expected_tele_rotor4 = tele_gear_sum >= 13

    if actual_auto_rotor1 != expected_auto_rotor1:
        error_messages.append((alliance_color + "Auto Rotor 1", actual_auto_rotor1, "%s (sum=%s)" % (expected_auto_rotor1, auto_gear_sum)))

    if actual_auto_rotor2 != expected_auto_rotor2:
        error_messages.append((alliance_color + "Auto Rotor 2", actual_auto_rotor2, "%s (sum=%s)" % (expected_auto_rotor2, auto_gear_sum)))

    if actual_tele_rotor1 != expected_tele_rotor1:
        error_messages.append((alliance_color + "Tele Rotor 1", actual_tele_rotor1, "%s (sum=%s)" % (expected_tele_rotor1, tele_gear_sum)))

    if actual_tele_rotor2 != expected_tele_rotor2:
        error_messages.append((alliance_color + "Tele Rotor 2", actual_tele_rotor2, "%s (sum=%s)" % (expected_tele_rotor2, tele_gear_sum)))

    if actual_tele_rotor3 != expected_tele_rotor3:
        error_messages.append((alliance_color + "Tele Rotor 3", actual_tele_rotor3, "%s (sum=%s)" % (expected_tele_rotor3, tele_gear_sum)))

    if actual_tele_rotor4 != expected_tele_rotor4:
        error_messages.append((alliance_color + "Tele Rotor 4", actual_tele_rotor4, "%s (sum=%s)" % (expected_tele_rotor4, tele_gear_sum)))

    #######################
    # Other
    #######################
    official_rope_sum = 0
    if official_sr.touchpadNear:
        official_rope_sum += 1
    if official_sr.touchpadMiddle:
        official_rope_sum += 1
    if official_sr.touchpadFar:
        official_rope_sum += 1

    official_baseline_sum = 0
    if official_sr.robot1Auto == "Mobility":
        official_baseline_sum += 1
    if official_sr.robot2Auto == "Mobility":
        official_baseline_sum += 1
    if official_sr.robot3Auto == "Mobility":
        official_baseline_sum += 1

    if official_rope_sum != climb_sum:
        error_messages.append((alliance_color + "Climbing", official_rope_sum, climb_sum))

    if official_baseline_sum != basline_sum:
        error_messages.append((alliance_color + "Baseline", official_baseline_sum, basline_sum))

    return warning_messages, error_messages


def validate_teams(match, official_match_srs):

    extra_teams = []
    missing_teams = []

#     match_srs = match.scoreresult_set.all()
#
#     if len(official_match_srs) == 2:
#         red_official = official_match_srs[0]
#         blue_official = official_match_srs[1]
#
#         for sr in match_srs:
#             if sr.team == red_official.team1:
#                 print "Got it!"
#         pass

    return extra_teams, missing_teams


def calculate_match_scouting_validity(match, official_match, official_match_srs):

    error_level = 0
    warning_messages = []
    error_messages = []

    validate_teams(match, official_match_srs)

    if len(official_match_srs) == 2:
        red_official = official_match_srs[0]
        blue_official = official_match_srs[1]

        red_teams, red_missing = get_teams_sr("Red", match, match.red1, match.red2, match.red3, red_official)
        blue_teams, blue_missing = get_teams_sr("Blue", match, match.blue1, match.blue2, match.blue3, blue_official)

        match_srs = [sr.team for sr in match.scoreresult_set.all()]
        teams_required = set([match.red1, match.red2, match.red3, match.blue1, match.blue2, match.blue3])

        duplicate_teams = [item for item, count in collections.Counter(match_srs).items() if count > 1]
        extra_teams = set(match_srs).difference(teams_required)

        red_warning, red_error = validate_alliance_score("Red", red_teams, red_official)
        blue_warning, blue_error = validate_alliance_score("Blue", blue_teams, blue_official)

        warning_messages.extend(red_warning)
        warning_messages.extend(blue_warning)
        error_messages.extend(red_error)
        error_messages.extend(blue_error)

    if len(red_missing) != 0 or len(blue_missing) != 0 or len(duplicate_teams) != 0 or len(extra_teams) != 0:
        error_level = 3
    elif len(error_messages) != 0:
        error_level = 2
    elif len(warning_messages) != 0:
        error_level = 1

    return error_level, red_missing, blue_missing, duplicate_teams, extra_teams, warning_messages, error_messages
