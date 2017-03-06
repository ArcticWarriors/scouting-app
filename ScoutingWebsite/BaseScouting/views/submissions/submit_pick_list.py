'''
Created on Mar 4, 2017

@author: PJ
'''

import json
from django.db import transaction
from django.http.response import HttpResponse
from django.views.generic.base import View


class BaseSubmitPickList(View):

    def __init__(self, groupings, competition_model, pick_list_model, team_model):
        self.groupings = groupings
        self.competition_model = competition_model
        self.pick_list_model = pick_list_model
        self.team_model = team_model

    @transaction.atomic
    def post(self, request, **kargs):
        success = False

        try:
            pick_list = json.loads(request.POST["pick_list"])
            competition = self.competition_model.objects.get(code=kargs['regional_code'])

            self.pick_list_model.objects.filter(competition=competition).delete()

            for grouping in self.groupings:

                for overall_pair in pick_list[grouping]:
                    rank = int(overall_pair[0])
                    team = self.team_model.objects.get(teamNumber=int(overall_pair[1]))
                    self.pick_list_model.objects.get_or_create(competition=competition, team=team, grouping=grouping, rank_in_group=rank)

            success = True
        except Exception as e:
            print e
    #
        output = {}
        output["success"] = success

        return HttpResponse(json.dumps(output), content_type='application/json')

