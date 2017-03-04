'''
Created on Mar 4, 2017

@author: PJ
'''

import json
from django.http.response import HttpResponse
from Scouting2017.model.reusable_models import PickList, Competition, Team
from django.db import transaction


@transaction.atomic
def submit_pick_list(request, **kwargs):

    success = False

    try:
        pick_list = json.loads(request.POST["pick_list"])
        competition = Competition.objects.get(code=kwargs['regional_code'])
        groupings = ["Overall", "Fuel", "Gear", "Defense", "Do Not Pick"]

        PickList.objects.filter(competition=competition).delete()

        for grouping in groupings:

            for overall_pair in pick_list[grouping]:
                rank = int(overall_pair[0])
                team = Team.objects.get(teamNumber=int(overall_pair[1]))
                PickList.objects.get_or_create(competition=competition, team=team, grouping=grouping, rank_in_group=rank)

        success = True
    except Exception as e:
        print e
#
    output = {}
    output["success"] = success

    return HttpResponse(json.dumps(output), content_type='application/json')
