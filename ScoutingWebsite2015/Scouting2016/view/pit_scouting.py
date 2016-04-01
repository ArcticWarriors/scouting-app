'''
Created on Mar 29, 2016

@author: PJ
'''

from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from Scouting2016.models import Team
from django.contrib.auth.decorators import permission_required
from Scouting2016.model.models2016 import TeamPitScouting


login_reverse = reverse_lazy('Scouting2016:showLogin')


@permission_required('auth.can_modify_model', login_url=login_reverse)
def info_for_pit_edit(request):
    return render(request, 'Scouting2016/pit_form/pre_pit_form.html')


@permission_required('auth.can_modify_model', login_url=login_reverse)
def show_add_pit(request):
    context = {}
    context['team'] = Team.objects.get(teamNumber=request.GET["team_number"])
    context['submit_pit'] = "/2016/submit_pit"
    return render(request, 'Scouting2016/pit_form/pit_form.html', context)


@permission_required('auth.can_modify_model', login_url=login_reverse)
def submit_new_pit(request):

    team_pit_scouting = TeamPitScouting.objects.get(team__teamNumber=request.POST['team_number'])
    team_pit_scouting.teamOrganized = request.POST['notes_organized']
    team_pit_scouting.teamLikeable = request.POST['notes_openness']
    team_pit_scouting.teamSwag = request.POST['notes_swag']
    team_pit_scouting.teamAwards = request.POST['notes_awards']
    team_pit_scouting.teamAlliances = request.POST['notes_alliances']
    team_pit_scouting.teamAlly174 = request.POST['ally_174']
    team_pit_scouting.teamOperational = request.POST['function']
    team_pit_scouting.teamOperationProblems = request.POST['notes_functionality']
    team_pit_scouting.teamFirstYear = request.POST['first_year']

    team_pit_scouting.drive = request.POST['drive']
    team_pit_scouting.Auto = request.POST['Auto']
    team_pit_scouting.ScoreHigh = request.POST['ScoreHigh']
    team_pit_scouting.ScoreLow = request.POST['ScoreLow']
    team_pit_scouting.portcullis = request.POST['portcullis']
    team_pit_scouting.cheval = request.POST['cheval']
    team_pit_scouting.moat = request.POST['moat']
    team_pit_scouting.ramparts = request.POST['ramparts']
    team_pit_scouting.sally = request.POST['sally']
    team_pit_scouting.drawbridge = request.POST['drawbridge']
    team_pit_scouting.rockwall = request.POST['rockwall']
    team_pit_scouting.rough = request.POST['rough']
    team_pit_scouting.lowBar = request.POST['lowBar']
    team_pit_scouting.scale = request.POST['scale']

    team_pit_scouting.save()

    return HttpResponseRedirect(reverse('Scouting2016:view_team', args=(team_pit_scouting.team.teamNumber,)))
