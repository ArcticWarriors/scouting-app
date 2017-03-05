'''
Created on Mar 1, 2017

@author: PJ
'''
from Scouting2017.model.reusable_models import Team
from Scouting2017.model.models2017 import TeamPitScouting
import json
from django.http.response import HttpResponse


def submit_pit_scouting(request, **kargs):

    success = False
    team_number = int(request.POST['team_number'])

    try:
        team = Team.objects.get(teamNumber=team_number)
        team_pit_scouting, _ = TeamPitScouting.objects.get_or_create(team=team)

        team_pit_scouting.OrganizedFunctional = request.POST['notes_functional']
        team_pit_scouting.FuelCapacity        = request.POST['notes_fuel_capacity']
        team_pit_scouting.Gears               = request.POST['notes_gears']
        team_pit_scouting.Strategy            = request.POST['notes_strategy']
        team_pit_scouting.Size                = request.POST['notes_size']
        team_pit_scouting.FuelAcquire         = request.POST['notes_acquire_fuel']
        team_pit_scouting.AllianceStrategy    = request.POST['notes_alliance_strategy']
        team_pit_scouting.AllanceCompetent    = request.POST['notes_alliacne_competence']
        team_pit_scouting.CompetnetConfident  = request.POST['notes_competent_confident']
        team_pit_scouting.Competitions        = request.POST['notes_compititions']
        team_pit_scouting.Random              = request.POST['notes_Misc']
        team_pit_scouting.save()
        success = True
    except Exception as e:
        print e

    return HttpResponse(json.dumps({"success": success}), content_type='application/json')
