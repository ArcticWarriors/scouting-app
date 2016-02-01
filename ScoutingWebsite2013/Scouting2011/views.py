from django.shortcuts import render
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Avg, Sum
from Scouting2011.models import Team, Match, ScoreResult


def __get_create_kargs(request):

    kargs = {}

    score_result_fields = ScoreResult.get_fields()

    for field_name in score_result_fields:
        if field_name not in request.POST:
            kargs[field_name] = score_result_fields[field_name].default
        else:
            kargs[field_name] = request.POST[field_name]

    return kargs


def index(request):

    our_team_number = 229

    our_team = Team.objects.get(teamNumber=our_team_number)
    our_scouted = Match.objects.filter(scoreresult__team__id=our_team.id)

    scouted_numbers = sorted([match.matchNumber for match in our_scouted])

    context = {}
    context['scouted_matches'] = scouted_numbers

    return render(request, 'Scouting2011/index.html', context)


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

        print context

    return render(request, 'Scouting2011/showGraph.html', context)


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
    return render(request, 'Scouting2011/RobotDisplay.html')


def view_team(request, team_number):
    this_team = Team.objects.get(teamNumber=team_number)

    metrics = this_team.get_metrics()
    score_result_list = []

    for sr in this_team.scoreresult_set.all():
        score_result_list.append(sr)

    context = {}
#     context['team_number'] = this_team.teamNumber
    context['metrics'] = metrics
    context['score_result_list'] = score_result_list
    context['team_number'] = team_number

    return render(request, 'Scouting2011/TeamPage.html', context)


def match_display(request, match_number):
    context = {}

    this_match = Match.objects.get(matchNumber=match_number)
    print this_match

    score_result_list = []

    for sr in this_match.scoreresult_set.all():
        score_result_list.append(sr)

    context['score_result_list'] = score_result_list
    context['match_display'] = match_number
    return render(request, 'Scouting2011/MatchPage.html', context)


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

    return render(request, 'Scouting2011/AllTeams.html', context)


def all_matches(request):
    matches = Match.objects.all()

    context = {}
    context['scouted_matches'] = matches

    return render(request, 'Scouting2011/AllMatches.html', context)


def search_page(request):

    def __get_annotate_args(score_result_field):
        if score_result_field.metric_type == "Average":
            return score_result_field.display_name, Avg('scoreresult__' + score_result_field.field_name)
        else:
            return score_result_field.display_name, Sum('scoreresult__' + score_result_field.field_name)

    def __get_filter_args(score_result_field, sign, value):

        django_value = ""
        if sign == '>=':
            django_value = "__gte"
        if sign == '<=':
            django_value = "__lte"

        return "%s%s" % (display_name, django_value), value

    context = {}

    # This would imply that they were on the search page, and made a request
    if len(request.GET) != 0:
        context['get'] = request.GET

        annotate_args = {}
        filter_args = {}
        good_fields = []

        valid_fields = []
        for score_result_field in ScoreResult.get_fields().values():
            field_name = score_result_field.field_name
            value_key = field_name + "_value"

            if field_name in request.GET and value_key in request.GET:
                value = request.GET[field_name]
                sign = request.GET[value_key]
                if len(value) != 0 and len(sign) != 0:

                    valid_fields.append(score_result_field)
                    display_name = score_result_field.display_name
                    annotate = __get_annotate_args(score_result_field)
                    filter_arg = __get_filter_args(score_result_field, sign, value)

                    annotate_args[annotate[0]] = annotate[1]
                    filter_args[filter_arg[0]] = filter_arg[1]
                    good_fields.append(score_result_field)
#
        search_results = Team.objects.all().annotate(**annotate_args).filter(**filter_args)
#
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

        context['results'] = results

    return render(request, 'Scouting2011/search.html', context)
