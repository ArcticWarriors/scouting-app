'''
Created on Mar 5, 2017

@author: PJ
'''
from django.db.models.aggregates import Avg, Sum
from django.db.models.expressions import Case, When


def get_team_metrics(team, regional_code):
    metrics = team.scoreresult_set.filter(competition__code=regional_code).aggregate(
                                             Avg("auto_fuel_high_score"),
                                             Avg("auto_fuel_high_shots"),
                                             Avg("auto_fuel_low_score"),
                                             Avg("auto_fuel_low_shots"),
                                             Avg("auto_gears"),

                                             Avg("tele_fuel_high_score"),
                                             Avg("tele_fuel_high_shots"),
                                             Avg("tele_fuel_low_score"),
                                             Avg("tele_fuel_low_shots"),
                                             Avg("tele_gears"),

                                             Sum("foul"),
                                             Sum("tech_foul"),
                                             Sum("yellow_card"),
                                             Sum("red_card"),

                                             rope__avg=Avg(Case(When(rope=True, then=1), When(rope=False, then=0))),
                                             baseline__avg=Avg(Case(When(auto_baseline=True, then=1), When(auto_baseline=False, then=0))),
                                             )

    # Format all of the numbers.  If we haven't scouted the team, None will be returned.  Turn that into NA
    for key in metrics:
        if metrics[key] == None:
            metrics[key] = "NA"
        elif "__avg" in key:
            metrics[key] = "{:10.2f}".format(metrics[key])

    if metrics['tele_fuel_high_score__avg'] != "NA":

        metrics['auto_fuel_high_misses__avg'] = float(metrics['auto_fuel_high_shots__avg']) - float(metrics['auto_fuel_high_score__avg'])
        metrics['auto_fuel_low_misses__avg'] = float(metrics['auto_fuel_low_shots__avg']) - float(metrics['auto_fuel_low_score__avg'])

        metrics['tele_fuel_high_misses__avg'] = float(metrics['tele_fuel_high_shots__avg']) - float(metrics['tele_fuel_high_score__avg'])
        metrics['tele_fuel_low_misses__avg'] = float(metrics['tele_fuel_low_shots__avg']) - float(metrics['tele_fuel_low_score__avg'])
    else:
        metrics['auto_fuel_high_misses__avg'] = "NA"
        metrics['auto_fuel_low_misses__avg'] = "NA"

        metrics['tele_fuel_high_misses__avg'] = "NA"
        metrics['fuel_shot_low_missed__avg'] = "NA"

    return metrics
