from Scouting2016.model.reusable_models import Team, Competition, Match
from Scouting2016.model.models2016 import ScoreResult
from django.shortcuts import render


def __get_create_kargs(request):
    """
    Fill out a list of kargs based on the given request and its POST arguments.
    Will iterate over all of the allowable ScoreResult fields, and will add an
    item into the kargs dicitionary for each one, using the fields default value
    if it is not present in POST.  The result will be a dictionary of
    field_name -> integer value

    @param request: The request containing the POST dictionary

    @return: A dictionary containing field -> value pairs
    """

    kargs = {}

    score_result_fields = ScoreResult.get_fields()

    for field_name in score_result_fields:
        if field_name not in request.POST:
            kargs[field_name] = score_result_fields[field_name].default
        else:
            kargs[field_name] = request.POST[field_name]

    return kargs


def submit_new_match(request, regional_code):
    """
    Creates a new score result and match (if possible).  Uses the team and match number
    from the form to search for an existing score result.  If one exists, it will
    re-direct the user back to the form so they can attempt to input the data again.

    If the score result does not exist, a new one will be created
    """

    team = Team.objects.get(teamNumber=request.POST["team_number"])
    competition = Competition.objects.get(code=regional_code)
    if len(Match.objects.filter(matchNumber=request.POST["match_number"])) == 0:
        match = Match.objects.create(matchNumber=request.POST["match_number"], competition=competition)
    else:
        match = Match.objects.get(matchNumber=request.POST["match_number"])

    available_srs = ScoreResult.objects.filter(match=match, team=team)

    # score result with this combination already exists, don't let them add it again
    kargs = __get_create_kargs(request)
    keys = sorted(kargs.keys())
    print("\n".join("%s->%s" % (key, kargs[key]) for key in keys))
    if len(available_srs) != 0:
        context = {}
        context['error_message'] = "ERROR! A combination of team %s and match %s already exists" % (team.teamNumber, match.matchNumber)
        context['match_number'] = match.matchNumber
        context['team_number'] = team.teamNumber
        context['submit_view'] = "/2016/submit_form"

        fake_score_result = {}
        for key in request.POST:
            fake_score_result[key] = request.POST[key]
        context['sr'] = fake_score_result

        return render(request, 'Scouting2016/inputForm.html', context)
    else:
        kargs = __get_create_kargs(request)
        ScoreResult.objects.create(match=match, team=team, competition=competition, **kargs)
