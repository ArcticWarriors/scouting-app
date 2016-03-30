import operator

from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models.aggregates import Avg, Sum
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from Scouting2016.models import Team, Match, ScoreResult, TeamPictures, OfficialMatch, TeamComments
from django.contrib.auth.decorators import permission_required
from Scouting2016.model.models2016 import get_team_metrics


login_reverse = reverse_lazy('Scouting2016:showLogin')


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


def show_graph(request):
    context = {}
    context['teams'] = Team.objects.all()

    """
    request.GET contains all the information of which checkboxes are checked.
    If no checkboxes are checked, the length will be zero and the graphing script will not run
    """
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
        """
        graph_url calls the gen_graph function to graph all the teams and the fields using matplotlib
        selected_teams and selected_fields are joined together into a single string which can be
        placed into the URL
        """
    return render(request, 'Scouting2016/showGraph.html', context)



def view_team(request, team_number):

    """
    This page will show detailed information on any team requested.
    Users are able to view total defense crosses for the team, along with more permanent field
    elements ( high goal, autonomous scores, tech fouls, etc) with a per match average
    @param team_number is the team number for the team requested to be displayed
    """

    this_team = Team.objects.get(teamNumber=team_number)
    picture_list = TeamPictures.objects.filter(team_id=this_team.id)
    """
    The page will return a list of score results stored in the database. Score results are stored in
    either sums or averages, as defined in the model. The page is also able to upload and store pictures,
    using a naming convention of picture_### to store and display all avalable pictures on the website itself.
    """

    metrics = get_team_metrics(this_team)
    score_result_list = []

    for sr in this_team.scoreresult_set.all():
        score_result_list.append(sr)

    team_comments_search = TeamComments.objects.filter(team=this_team)

    context = {}
#     context['team_number'] = this_team.teamNumber
    context['team'] = this_team
    context['metrics'] = metrics
    context['score_result_list'] = score_result_list
    context['team_number'] = team_number
    context['pictures'] = picture_list
    if len(team_comments_search) != 0:
        context['team_comments'] = team_comments_search.all()

    return render(request, 'Scouting2016/TeamPage.html', context)


def get_sorted_defense_stats(teams):
    results = {}

    for team in teams:
        team.get_defense_stats(results)

    for category in results:
        results[category] = sorted(results[category].items(), key=operator.itemgetter(1), reverse=True)

    return sorted(results.items())


def match_prediction(request, match_number):

    """
    This page is displayed when a match which has not happened yet would be requested
    the page is useful for upcoming matches, as it can display which defenses each ALLIANCE
    crosses the most and the least (ecxluding the low bar, since it will always be on the field
    and is irrelevant for our purposes) by obtaining information from get_defnese_stats, and addimg
    the total crosses from each team into a grand total. This total is then sorted into a ranked
    list by using the sorted() function with reverse=true.
    @param match_number is the match which is being predicted.
    """

    official_match = OfficialMatch.objects.get(matchNumber=match_number)
    score_results = official_match.officialmatchscoreresult_set.all()
    red_results = score_results[0]
    blue_results = score_results[1]

    context = {}
    context['match_number'] = match_number
    context['red_results'] = red_results
    context['blue_results'] = blue_results
#     context['audience_defense'] = official_match.audienceSelectionCategory

#     red_teams = [official_match.redTeam1, official_match.redTeam2, official_match.redTeam3]
#     blue_teams = [official_match.blueTeam1, official_match.blueTeam2, official_match.blueTeam3]
#
#     red_prediction, blue_prediction = official_match.predict_score()
#
#     context['red_defenses'] = get_sorted_defense_stats(red_teams)
#     context['blue_defenses'] = get_sorted_defense_stats(blue_teams)
#     context['red_prediction'] = red_prediction
#     context['blue_prediction'] = blue_prediction

    return render(request, 'Scouting2016/view_official_match.html', context)


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

            if field_name == 'scale_challenge' or field_name == 'auto_defense':
                continue
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
        team_numbers = [team_result.teamNumber for team_result in search_results]

        filtered_results = __create_filtered_team_metrics(search_results, good_fields)

        if 'scale_challenge' in request.GET:
            filtered_results = search_result_filter(request, team_numbers, filtered_results, 'scale_challenge')

        if 'auto_defense' in request.GET:
            filtered_results = search_result_filter(request, team_numbers, filtered_results, 'auto_defense')

        context['results'] = filtered_results
    return render(request, 'Scouting2016/search.html', context)


def search_result_filter(request, team_numbers, filtered_results, parameter):

    if parameter in request.GET:
        kargs = {}
        kargs[parameter] = request.GET[parameter]
        all_teams_that_passes_parameter = ScoreResult.objects.filter(team__teamNumber__in=team_numbers).filter(**kargs)

    print all_teams_that_passes_parameter
    team_that_passes_parameter = [sr.team.teamNumber for sr in all_teams_that_passes_parameter]
    final_result = []
    for team_score_results in filtered_results:
        team_tuple = team_score_results[0]
        this_team_number = team_tuple[1]

        if this_team_number in team_that_passes_parameter:
            final_result.append(team_score_results)
#             print "Team %s passed" % (team_score_results)
#         else:
#             print "Team %s failed" % (this_team_number)

    return final_result

#######################################
# Form Stuff
#######################################

    # Pit stuff


def get_hovercard(request):
    context = {}
    the_type = request.GET.get('type')
    if the_type == "colSelectContent":
        return render(request, 'Scouting2016/hovercards/colSelectContent.html')
    elif the_type == "filterContent":
        context['filterType'] = request.GET.get('filterType')
        return render(request, 'Scouting2016/hovercards/filterContent.html', context)


def bookmark_team_page(request):
    team = Team.objects.get(teamNumber=request.POST['team_number'])
    team.bookmark = request.POST['bookmark']
    team.save()
    return HttpResponseRedirect(reverse('Scouting2016:view_team', args=(team.teamNumber,)))
