from Scouting2017.model.models2017 import ScoreResult
from django.db.models.aggregates import Avg
from django.db.models.expressions import Case, When
import json
import math
import collections


def get_statistics(regional_code, teams_at_competition, team=0):
    '''
    The get_statistics function() returns two lists of metrics.
    The first thing it returns, stats, is a dictionary containing the values of overall averages for all score results, along with standard deviations for those same score results along the mean.
    The function also returns a list called skills, which contains data for each team including their z-scores, calculated fuel scores for both hi, low, autonomous, teleop, and overall, and their accuracy in climbing the rope.
    '''

    skills = []

    competition_srs = ScoreResult.objects.filter(competition__code=regional_code)
    competition_averages = competition_srs.aggregate(Avg('auto_gears'),
                                                     Avg('auto_fuel_high_score'),
                                                     Avg('auto_fuel_low_score'),
                                                     Avg('tele_gears'),
                                                     Avg('tele_fuel_high_score'),
                                                     Avg('tele_fuel_low_score'),
                                                     rope__avg=Avg(Case(When(rope=True, then=1), When(rope=False, then=0))))
    rope_avg = competition_averages['rope__avg']
    gear_avg = competition_averages['tele_gears__avg']

    if competition_averages['auto_fuel_high_score__avg'] and competition_averages['tele_fuel_high_score__avg'] and competition_averages['auto_fuel_low_score__avg'] and competition_averages['tele_fuel_low_score__avg']:

        fuel_avg = competition_averages['auto_fuel_high_score__avg'] + (competition_averages['tele_fuel_high_score__avg'] / 3) + (competition_averages['auto_fuel_low_score__avg'] / 3) + (competition_averages['tele_fuel_low_score__avg'] / 9)
    else:
        fuel_avg = 0

    # This part of the function (above) obtains overall averages for all score results
    gear_v2 = 0
    fuel_v2 = 0
    rope_v2 = 0
    num_srs = 0

    for sr in competition_srs:
        if sr.rope:
            sr_rope = 1 - rope_avg
        else:
            sr_rope = 0 - rope_avg
        sr_gear = sr.tele_gears - gear_avg
        sr_fuel = ((sr.auto_fuel_high_score) + (sr.tele_fuel_high_score / 3) + (sr.auto_fuel_low_score / 3) + (sr.tele_fuel_low_score / 9)) - fuel_avg
        gear_v2 += sr_gear * sr_gear
        fuel_v2 += sr_fuel * sr_fuel
        rope_v2 += sr_rope * sr_rope
        num_srs += 1

    if num_srs == 0:
        gear_stdev = 0
        fuel_stdev = 0
        rope_stdev = 0
    else:
        gear_stdev = math.sqrt(gear_v2 / num_srs)
        fuel_stdev = math.sqrt(fuel_v2 / num_srs)
        rope_stdev = math.sqrt(rope_v2 / num_srs)

    team_avgs = collections.defaultdict(int)

    # This part of the function (above) obtains overall standard deviations for all score results
    teams = team if bool(team) else teams_at_competition
    print teams
    for team in teams:
        teams_srs = team.scoreresult_set.filter(competition__code=regional_code)
        team_avgs = teams_srs.aggregate(Avg('tele_gears'),
                                        Avg('tele_fuel_high_score'),
                                        Avg('auto_fuel_high_score'),
                                        Avg('tele_fuel_low_score'),
                                        Avg('auto_fuel_low_score'),
                                        team_rope__avg=Avg(Case(When(rope=True, then=1), When(rope=False, then=0))))

        team.skills = {}
        team.skills['fuel_z'] = 'NA'
        team.skills['gear_z'] = 'NA'
        team.skills['rope_z'] = 'NA'
        team.skills['rope_pct'] = 'NA'
        if len(teams_srs) != 0:
            team.skills['fuel_score'] = ((team_avgs['auto_fuel_high_score__avg']) + (team_avgs['tele_fuel_high_score__avg'] / 3) + (team_avgs['auto_fuel_low_score__avg'] / 3) + (team_avgs['tele_fuel_low_score__avg'] / 9))
            team.skills['gear_z'] = (team_avgs['tele_gears__avg'] - gear_avg) / gear_stdev if gear_stdev != 0 else 0
            team.skills['fuel_z'] = (((team_avgs['auto_fuel_high_score__avg']) + (team_avgs['tele_fuel_high_score__avg'] / 3) + (team_avgs['auto_fuel_low_score__avg'] / 3) + (team_avgs['tele_fuel_low_score__avg'] / 9)) - fuel_avg) / fuel_stdev if fuel_stdev != 0 else 0
            team.skills['rope_z'] = (team_avgs['team_rope__avg'] - rope_avg) / rope_stdev if rope_stdev != 0 else 0
            team.skills['rope_pct'] = team_avgs['team_rope__avg'] * 100

        skills.append({'team': team.teamNumber, 'skills': team.skills})

    stats = {'gear_avg': gear_avg, 'rope_avg': rope_avg, 'fuel_avg': fuel_avg, 'fuel_hi_avg': team_avgs['tele_fuel_high_score__avg'], 'fuel_low_avg': team_avgs['tele_fuel_low_score__avg'],
             'fuel_hi_auto_avg': team_avgs['auto_fuel_high_score__avg'], 'fuel_low_auto_avg': team_avgs['auto_fuel_low_score__avg'], 'auto_gear_avg': competition_averages['auto_gears__avg'], 'gear_stdev': gear_stdev, 'rope_stdev': rope_stdev, 'fuel_stdev': fuel_stdev}

    return (stats, json.dumps(skills))
