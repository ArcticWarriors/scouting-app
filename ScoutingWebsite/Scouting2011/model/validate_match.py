'''
Created on Mar 4, 2017

@author: preiniger
'''


def __validate_alliance(alliance_color, teams, official_sr):
    team1sr = None
    team2sr = None
    team3sr = None

    # TODO: there has to be a better way... but I'd rather not touch the DB
    for sr in teams[0].scoreresult_set.all():
        if sr.match.matchNumber == official_sr.official_match.matchNumber:
            team1sr = sr
            break

    for sr in teams[1].scoreresult_set.all():
        if sr.match.matchNumber == official_sr.official_match.matchNumber:
            team2sr = sr
            break

    for sr in teams[2].scoreresult_set.all():
        if sr.match.matchNumber == official_sr.official_match.matchNumber:
            team3sr = sr
            break
        
    team_srs = [team1sr, team2sr, team3sr]
    team_srs = [sr for sr in team_srs if sr != None]
    
    warning_messages = []
    error_messages = []
    
    for team in teams:
        if team != official_sr.team1 and team != official_sr.team2 and team != official_sr.team3:
            error_messages.append((alliance_color + " team mismatch", teams, team.teamNumber))
            
    if len(team_srs) != 3:
        error_messages.append((alliance_color + " wrong number of teams", 3, len(team_srs)))
        
    tele_high_tubes = 0
    tele_mid_tubes = 0
    tele_low_tubes = 0
    
    
    for sr in team_srs:
        tele_high_tubes += sr.high_tubes_hung
        tele_mid_tubes += sr.mid_tubes_hung
        tele_low_tubes += sr.low_tubes_hung
        
    total_score = tele_high_tubes * 3 + tele_mid_tubes * 2 + tele_low_tubes
    
    if total_score != official_sr.total_score:
        warning_messages.append((alliance_color + " total score", official_sr.total_score, total_score))
        

    return warning_messages, error_messages

def validate_match(match, official_match, official_srs):
    
    error_level = 0
    warning_messages = []
    error_messages = []

    red_teams = [match.red1, match.red2, match.red3]
    blue_teams = [match.blue1, match.blue2, match.blue3]
    
    red_sr = official_srs[0]
    blue_sr = official_srs[1]
    
    red_warning, red_error = __validate_alliance("Red", red_teams, red_sr)
    blue_warning, blue_error = __validate_alliance("Blue", blue_teams, blue_sr)

    warning_messages.extend(red_warning)
    warning_messages.extend(blue_warning)
    error_messages.extend(red_error)
    error_messages.extend(blue_error)
    

    if len(error_messages) != 0:
        error_level = 2
    elif len(warning_messages) != 0:
        error_level = 1

    return error_level, warning_messages, error_messages
