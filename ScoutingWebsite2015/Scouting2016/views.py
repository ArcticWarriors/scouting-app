import os

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db.models.aggregates import Avg, Sum
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from Scouting2016.models import Team, Match, ScoreResult, TeamPictures, \
    OfficialMatch


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


def __create_filtered_team_metrics(search_results, good_fields):
    """
    Iterates over a set of annotates results from a team search.
    Using the good_fields parameters, it will fill out the results
    field.  The result will look like this

    [
      [('Team Number', 174), ('SR Field 1', 2.50), ('SR Field 2', 8.78)]
      [('Team Number', 229), ('SR Field 1', 0.00), ('SR Field 2', 2.90)]
    ]

    This way, you can iterate over all of the results and populate the
    template with the field name and field value
    """

    results = []

    for result in search_results:
        team_result = []
        team_result.append(("Team Number", result.teamNumber))

        for field in good_fields:
            value = getattr(result, field.display_name)
            if field.metric_type == "Average":
                value = "{:10.2f}".format(value)
            team_result.append((field.display_name, value))

        results.append(team_result)

    return results


def __get_annotate_args(score_result_field):
    """
    Gets the argument pair that can be used in a model.annotate() call.
    Will call either the Avg() annotation, or the Sum() annotation.  The re-named
    field will be the score result fields display name

    Example Output:
    ("Total Score", Avg('scoreresult__total_score'))

    """

    if score_result_field.metric_type == "Average":
        return score_result_field.display_name, Avg('scoreresult__' + score_result_field.field_name)
    else:
        return score_result_field.display_name, Sum('scoreresult__' + score_result_field.field_name)


def __get_filter_args(score_result_field, sign, value):
    """
    Gets the arguments that can be used in a model.fiter() call.
    Based on the given sign, this will append the display name
    of the score result with the appropriate filter extension

    Examples:
       "TotalScore__lte" # sign is >=
       "TotalScore__gte" # sign is <=
       "TotalScore"      # sign is =
   """

    django_value = ""
    if sign == '>=':
        django_value = "__gte"
    if sign == '<=':
        django_value = "__lte"

    return "%s%s" % (score_result_field.display_name, django_value), value


def index(request):

    our_team_number = 174

    our_team = Team.objects.get(teamNumber=our_team_number)
    our_scouted = Match.objects.filter(scoreresult__team__id=our_team.id)
    our_official = OfficialMatch.objects.filter(Q(redTeam1=our_team_number) |
                                                Q(redTeam2=our_team_number) |
                                                Q(redTeam3=our_team_number) |
                                                Q(blueTeam1=our_team_number) |
                                                Q(blueTeam2=our_team_number) |
                                                Q(blueTeam3=our_team_number))
    all_official_numbers = set(match.matchNumber for match in our_official)

    scouted_numbers = sorted([match.matchNumber for match in our_scouted])
    unscouted_numbers = all_official_numbers.difference(scouted_numbers)

    context = {}
    context['scouted_matches'] = scouted_numbers
    context['unscouted_matches'] = sorted([x for x in unscouted_numbers])

    return render(request, 'Scouting2016/index.html', context)


def show_graph(request):
    context = {}
    context['teams'] = Team.objects.all()

    # This implies they are trying to look for a graph
    if len(request.GET) != 0:

        teams = []
        fields = []

        for key in request.GET:
            try:
                team_number = int(key)
                teams.append(team_number)
            except:
                fields.append(key)

        context['selected_fields'] = ",".join(fields)
        context['selected_fields_list'] = [str(x) for x in fields]
        context['selected_teams'] = ",".join(str(x) for x in teams)
        context['selected_teams_list'] = teams
        context['graph_url'] = 'gen_graph/%s/%s' % (context['selected_teams'], context['selected_fields'])

    return render(request, 'Scouting2016/showGraph.html', context)


def gen_graph(request, team_numbers, fields):

    import matplotlib
    matplotlib.use('agg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.font_manager import FontProperties

    team_numbers = [int(x) for x in team_numbers.split(",")]
    fields = fields.split(',')

    f = plt.figure(figsize=(6, 6))
    legend_handles = []

    for team_number in team_numbers:
        team = Team.objects.get(teamNumber=int(team_number))

        for field in fields:
            metric = []
            for result in team.scoreresult_set.all():
                metric.append(getattr(result, field))

            hand, = plt.plot(metric, label="Team %s, %s" % (team.teamNumber, field))
            legend_handles.append(hand)

    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(handles=legend_handles, prop=fontP)
    plt.xlabel("Match")

    matplotlib.pyplot.close(f)

    canvas = FigureCanvasAgg(f)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)

    return response

    pass


def robot_display(request):
    return render(request, 'Scouting2016/RobotDisplay.html')


def view_team(request, team_number):
    this_team = Team.objects.get(teamNumber=team_number)
    picture_list = TeamPictures.objects.filter(team_id=this_team.id)

    metrics = this_team.get_metrics()
    score_result_list = []

    for sr in this_team.scoreresult_set.all():
        score_result_list.append(sr)

    context = {}
#     context['team_number'] = this_team.teamNumber
    context['metrics'] = metrics
    context['score_result_list'] = score_result_list
    context['team_number'] = team_number
    context['pictures'] = picture_list

    return render(request, 'Scouting2016/TeamPage.html', context)


def match_display(request, match_number):
    context = {}

    this_match = Match.objects.get(matchNumber=match_number)

    score_result_list = []

    for sr in this_match.scoreresult_set.all():
        score_result_list.append(sr)

    context['score_result_list'] = score_result_list
    context['match_display'] = match_number
    return render(request, 'Scouting2016/MatchPage.html', context)


def match_prediction(request, match_number):

    official_match = OfficialMatch.objects.get(matchNumber=match_number)

    context = {}
    context['match_number'] = match_number
    context['red_team_1'] = Team.objects.get(teamNumber=official_match.redTeam1)
    context['red_team_2'] = Team.objects.get(teamNumber=official_match.redTeam2)
    context['red_team_3'] = Team.objects.get(teamNumber=official_match.redTeam3)
    context['blue_team_1'] = Team.objects.get(teamNumber=official_match.blueTeam1)
    context['blue_team_2'] = Team.objects.get(teamNumber=official_match.blueTeam2)
    context['blue_team_3'] = Team.objects.get(teamNumber=official_match.blueTeam3)

    return render(request, 'Scouting2016/MatchPrediction.html', context)


def all_teams(request):

    the_teams = Team.objects.all()

    teams_with_avg = []

    for team in the_teams:

        metrics = team.get_metrics()

        team_with_avg = {}
        team_with_avg["id"] = team.id
        team_with_avg["teamNumber"] = team.teamNumber
        team_with_avg["matches_scouted"] = team.scoreresult_set.count()
        team_with_avg["avgerages"] = metrics
        teams_with_avg.append(team_with_avg)

    context = {"teams": teams_with_avg}

    return render(request, 'Scouting2016/AllTeams.html', context)


def all_matches(request):
    matches = Match.objects.all()

    scouted_numbers = [match.matchNumber for match in matches]
    unscouted_matches = OfficialMatch.objects.all().exclude(matchNumber__in=scouted_numbers)

    context = {}
    context['scouted_matches'] = matches
    context['unscouted_matches'] = unscouted_matches

    return render(request, 'Scouting2016/AllMatches.html', context)


def search_page(request):

    context = {}

    # This would imply that they were on the search page, and made a request
    if len(request.GET) != 0:
        context['get'] = request.GET

        annotate_args = {}
        filter_args = {}
        good_fields = []

        valid_fields = []

        # For each available field, check if the GET request has the field AND the field sign
        for score_result_field in ScoreResult.get_fields().values():
            field_name = score_result_field.field_name
            value_key = field_name + "_value"

            if field_name in request.GET and value_key in request.GET:
                value = request.GET[field_name]
                sign = request.GET[value_key]

                # If it does have both fields, make sure they are not empty.  If they are empty, they are worthless
                if len(value) != 0 and len(sign) != 0:

                    valid_fields.append(score_result_field)
                    annotate = __get_annotate_args(score_result_field)
                    filter_arg = __get_filter_args(score_result_field, sign, value)

                    annotate_args[annotate[0]] = annotate[1]
                    filter_args[filter_arg[0]] = filter_arg[1]
                    good_fields.append(score_result_field)
#
        """
        BLACK MAGIC ALERT!!!

        Looking at this by itself makes seemingly no sense, but here is an example of what
        you might run from the command line to get the desired results:

        search_results = Team.objects.all().annotate(HighAuto_MyName=Avg("scoreresult__auto_score_high")).filter(HighAuto_MyName__gte=5)

        The first call, annotate, will create the average results that we will want to filter on.  We can re-name the result
        to "HighAuto_MyName" so that we can use it later.

        The second call, filter, will use the name we created earlier, "HighAuto_MyName" to run a greater-than-or-equal-to comparison,
        and give us a list of the teams that pass the requirements

        search_results now contains a list of the teams that passed the filter.  Furthermore, since we re-named our field during the
        annotate phase, a new, fake field has been added to our team object.  We could do search_results[0].HighAuto_MyName to print
        out how many high auto goals the team scores on average
        """
        search_results = Team.objects.all().annotate(**annotate_args).filter(**filter_args)
        context['results'] = __create_filtered_team_metrics(search_results, good_fields)

    return render(request, 'Scouting2016/search.html', context)


def upload_image(request):

    team_numer = request.POST['team_number']
    f = request.FILES['image_name']

    static_dir = 'Scouting2016/static/'
    out_file_name = static_dir + 'Scouting2016/teambotimages/%s_{0}%s' % (team_numer, os.path.splitext(f.name)[1])

    # Look for the next available number, i.e. if there are [#_0, #_1, ..., #_10], this would make the new picture #_11
    picture_number = 0
    found = False
    while not found:
        test_name = out_file_name.format(picture_number)
        if not os.path.exists(test_name):
            out_file_name = test_name
            found = True
        else:
            picture_number += 1

    team = Team.objects.get(teamNumber=team_numer)
    TeamPictures.objects.create(team=team, path=out_file_name[len(static_dir):])

    # Write the file to disk
    with open(out_file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return HttpResponseRedirect(reverse('Scouting2016:view_team', args=(team_numer,)))

#######################################
# Form Stuff
#######################################


def info_for_form_edit(request):

    return render(request, 'Scouting2016/info_for_form_edit.html')


def show_add_form(request):

    context = {}
    context['team_number'] = 1765
    context['match_number'] = 10
    context['submit_view'] = "/2016/submit_form"
    context["sr"] = {}

    score_result_fields = ScoreResult.get_fields()
    for field_name, value in score_result_fields.iteritems():
        context["sr"][field_name] = value.default

    return render(request, 'Scouting2016/inputForm.html', context)


def show_edit_form(request):

    match = Match.objects.get(matchNumber=request.GET["match_number"])
    team = Team.objects.get(teamNumber=request.GET["team_number"])

    score_results = ScoreResult.objects.get(match_id=match.id, team_id=team.id)
    print score_results

    context = {}
    context['team_number'] = request.GET["team_number"]
    context['match_number'] = request.GET["match_number"]
    context['sr'] = score_results
    context['submit_view'] = '/2016/submit_edit'
    context['lock_team_and_match'] = True

    return render(request, 'Scouting2016/inputForm.html', context)


def submit_new_match(request):
    """
    Creates a new score result and match (if possible).  Uses the team and match number
    from the form to search for an existing score result.  If one exists, it will
    re-direct the user back to the form so they can attempt to input the data again.

    If the score result does not exist, a new one will be created
    """

    team = Team.objects.get(teamNumber=request.POST["team_number"])
    if len(Match.objects.filter(matchNumber=request.POST["match_number"])) == 0:
        match = Match.objects.create(matchNumber=request.POST["match_number"])
    else:
        match = Match.objects.get(matchNumber=request.POST["match_number"])

    available_srs = ScoreResult.objects.filter(match=match, team=team)

    # score result with this combination already exists, don't let them add it again
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
        ScoreResult.objects.create(match=match, team=team, **kargs)

        return HttpResponseRedirect(reverse('Scouting2016:match_display', args=(match.matchNumber,)))


def edit_prev_match(request):
    """
    Edits an existing match.
    """

    match = Match.objects.get(matchNumber=request.POST["match_number"])
    team = Team.objects.get(teamNumber=request.POST["team_number"])

    score_result = ScoreResult.objects.get(match_id=match.id, team_id=team.id)

    sr_fields = request.POST
    for key, value in sr_fields.iteritems():
        setattr(score_result, key, value)
    score_result.save()

    context = {}
    context['match_display'] = match.matchNumber

    return HttpResponseRedirect(reverse('Scouting2016:match_display', args=(match.matchNumber,)))
