from Scouting2016.model.reusable_models import Match, Team
from Scouting2016.model.models2016 import ScoreResult
from django.shortcuts import render


def show_edit_form(request, regional_code):

    match = Match.objects.get(matchNumber=request.GET["match_number"])
    team = Team.objects.get(teamNumber=request.GET["team_number"])

    score_results = ScoreResult.objects.get(match_id=match.id, team_id=team.id)
    print(score_results)

    context = {}
    context["regional_code"] = regional_code
    context['team_number'] = request.GET["team_number"]
    context['match_number'] = request.GET["match_number"]
    context['sr'] = score_results
    context['submit_view'] = '/2016/submit_edit'
    if request.user.username != 'scoutmaster':
        context['lock_team_and_match'] = True

    return render(request, 'Scouting2016/match_form/match_form.html', context)
