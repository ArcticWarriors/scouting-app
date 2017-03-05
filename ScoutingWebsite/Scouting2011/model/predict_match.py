'''
Created on Mar 3, 2017

@author: PJ
'''
from django.db.models.aggregates import Avg
from django.db.models.expressions import Case, When


def __get_team_average_for_match_prediction(team, competition):

    output = {}

    output["team_number"] = team.teamNumber

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

    return output


def predict_match(match, competition):

    output = {}

    output['red_prediction'] = __get_alliance_average_for_match_prediction(match.red1, match.red2, match.red3, competition)
    output['blue_prediction'] = __get_alliance_average_for_match_prediction(match.blue1, match.blue2, match.blue3, competition)

    print output

    return output
