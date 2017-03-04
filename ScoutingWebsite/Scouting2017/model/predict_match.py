'''
Created on Mar 3, 2017

@author: PJ
'''
from django.db.models.aggregates import Avg
from django.db.models.expressions import Case, When


def __get_team_average_for_match_prediction(team, competition):

    output = team.scoreresult_set.filter(competition=competition).aggregate(
        auto_fuel_high=Avg("auto_fuel_high_score"),
        auto_fuel_low=Avg("auto_fuel_low_score"),
        auto_gears=Avg("auto_gears"),
        tele_fuel_high=Avg("tele_fuel_high_score"),
        tele_fuel_low=Avg("tele_fuel_low_score"),
        tele_gears=Avg("tele_gears"),
        baseline=Avg(Case(When(auto_baseline=True, then=1), When(auto_baseline=False, then=0))),
        rope=Avg(Case(When(rope=True, then=1), When(rope=False, then=0))))

    output["team_number"] = team.teamNumber

    fuel_total = output['auto_fuel_high'] + \
                 output['auto_fuel_low'] / 3.0 + \
                 output['tele_fuel_high'] / 3.0 + \
                 output['tele_fuel_low'] / 9.0

    output["fuel_total"] = fuel_total
    output["gear_total"] = output['auto_gears'] + output['tele_gears']
    output["total_score"] = fuel_total + output['baseline'] * 5 + output['rope'] * 50

    return output


def __get_alliance_average_for_match_prediction(team1, team2, team3, competition):

    team1_metrics = __get_team_average_for_match_prediction(team1, competition)
    team2_metrics = __get_team_average_for_match_prediction(team2, competition)
    team3_metrics = __get_team_average_for_match_prediction(team3, competition)

    averages = {}

    for key in team1_metrics.keys():
        averages[key] = float(team1_metrics[key]) + float(team2_metrics[key]) + float(team3_metrics[key])

    output = {}
    output['team1'] = team1_metrics
    output['team2'] = team2_metrics
    output['team3'] = team3_metrics
    output['averages'] = averages
    output['total_score'] = averages["total_score"]
    output['kpa_bonus'] = "Yes" if averages["fuel_total"] >= 40 else "No"
    output['rotor_bonus'] = "Yes" if averages["gear_total"] >= 40 else "No"

    return output


def predict_match(match, competition):

    output = {}

    output['red_prediction'] = __get_alliance_average_for_match_prediction(match.red1, match.red2, match.red3, competition)
    output['blue_prediction'] = __get_alliance_average_for_match_prediction(match.blue1, match.blue2, match.blue3, competition)

    return output
