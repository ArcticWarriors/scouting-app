'''
Created on Mar 1, 2017

@author: PJ
'''
# from Scouting2017.model.reusable_models import Team
from django.http.response import HttpResponseNotFound, HttpResponse
from django.views.generic.base import View
import json


class BaseUpdateBookmarks(View):

    def __init__(self, team_model):
        self.team_model = team_model

    def post(self, request, **kargs):

        if request.user == None or not request.user.is_authenticated():
            return HttpResponseNotFound('<h1>Must be logged in!</h1>')

        user = request.user
        team = self.team_model.objects.get(teamNumber=request.POST['team_number'])
        bookmark_type = request.POST["bookmark_type"]

        if bookmark_type == "bookmark":
            is_bookmarked = team in user.scout.bookmarked_teams.all()

            if is_bookmarked:
                user.scout.bookmarked_teams.remove(team)
            else:
                user.scout.bookmarked_teams.add(team)
        elif bookmark_type == "do_not_pick":
            is_bookmarked = team in user.scout.do_not_pick_teams.all()

            if is_bookmarked:
                user.scout.do_not_pick_teams.remove(team)
            else:
                user.scout.do_not_pick_teams.add(team)
        else:
            print "unknown bookmark type %s" % bookmark_type

        response = {'is_bookmarked': not is_bookmarked}

        return HttpResponse(json.dumps(response), content_type='application/json')
