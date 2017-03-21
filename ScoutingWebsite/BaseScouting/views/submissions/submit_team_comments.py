
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic.base import View


class BaseAddTeamCommentsView(View):

    def __init__(self, team_model, team_comments_model, reverse_name):
        self.team_model = team_model
        self.team_comments_model = team_comments_model
        self.reverse_name = reverse_name

    def post(self, request, **kwargs):

        regional_code = kwargs["regional_code"]
        team_number = kwargs["team_number"]
        comments = request.POST["team_comments"]

        team = self.team_model.objects.get(teamNumber=team_number)
        self.team_comments_model.objects.create(team=team, comment=comments)

        return HttpResponseRedirect(reverse(self.reverse_name, args=(regional_code, team_number,)))
