'''
Created on Mar 29, 2016

@author: PJ
'''

from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from Scouting2016.models import Team
from django.contrib.auth.decorators import permission_required


login_reverse = reverse_lazy('Scouting2016:showLogin')


@permission_required('auth.can_modify_model', login_url=login_reverse)
def info_for_pit_edit(request):
    return render(request, 'Scouting2016/info_for_pit_edit.html')


@permission_required('auth.can_modify_model', login_url=login_reverse)
def show_add_pit(request):
    team = request.GET["team_number"]
    print team
    context = {}
    context['team'] = Team.objects.get(teamNumber=team)
    context['submit_pit'] = "/2016/submit_pit"
    return render(request, 'Scouting2016/pitForm.html', context)


def submit_new_pit(request):
    team = Team.objects.get(teamNumber=request.POST['team_number'])
    team.teamOrganized = request.POST['notes_organized']
    team.teamLikeable = request.POST['notes_openness']
    team.teamSwag = request.POST['notes_swag']
    team.teamAwards = request.POST['notes_awards']
    team.teamAlliances = request.POST['notes_alliances']
    team.teamAlly174 = request.POST['ally_174']
    team.teamOperational = request.POST['function']
    team.teamOperationProblems = request.POST['notes_functionality']
    team.teamFirstYear = request.POST['first_year']

    team.drive = request.POST['drive']
    team.Auto = request.POST['Auto']
    team.ScoreHigh = request.POST['ScoreHigh']
    team.ScoreLow = request.POST['ScoreLow']
    team.portcullis = request.POST['portcullis']
    team.cheval = request.POST['cheval']
    team.moat = request.POST['moat']
    team.ramparts = request.POST['ramparts']
    team.sally = request.POST['sally']
    team.drawbridge = request.POST['drawbridge']
    team.rockwall = request.POST['rockwall']
    team.rough = request.POST['rough']
    team.lowBar = request.POST['lowBar']
    team.scale = request.POST['scale']

    team.save()

    return HttpResponseRedirect(reverse('Scouting2016:view_team', args=(team.teamNumber,)))
