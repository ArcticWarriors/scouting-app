import os

from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.db.models.aggregates import Avg, Sum
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from Scouting2016.models import Team, Match, ScoreResult, TeamPictures, OfficialMatch, \
    validate_match, TeamComments
import operator
from django.contrib.auth.decorators import login_required, permission_required


login_reverse = reverse_lazy('Scouting2016:showLogin')


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

    return render(request, 'Scouting2016/index.html')


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


def gen_graph(request, team_numbers, fields):

    """
    @param team_numbers is the list of all checked team numbers on the show_graph page.
    @param fields is the list of all checked fields on the show_graph page
    these two parameters determine what is graphed and displayed on the page
    """

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
    """
    gen_graph will create an image of whatever fields are selected with show_graph's request.GET
    it uses matplotlib to graph numbers on the Y axis and matches on the X axis
    Each field will be displayed with a different line color
    """

    return response

    pass


def show_comparison(request):

    context = {}
    context['teams'] = Team.objects.all()

    if len(request.GET) != 0:

        teams = []
        fields = []

        for key in request.GET:
            try:
                team_number = int(key)
                teams.append(team_number)
            except:
                fields.append(key)

        context['selected_team_numbers'] = teams
        context['selected_fields_names'] = [str(x) for x in fields]

    # This would imply that they were on the comparison page, and made a request
    if len(request.GET) != 0:
        context['get'] = request.GET

        annotate_args = {}
        good_fields = []

        valid_fields = []

        # For each available field, check if the GET request has the field AND the field sign
        for score_result_field in ScoreResult.get_fields().values():
            field_name = score_result_field.field_name

            if field_name in request.GET:
                value = request.GET[field_name]

                """
                Grabs whatever field names are requested, and if any fields are requested the
                following command blocks will be used
                """
                if len(value) != 0:

                    valid_fields.append(score_result_field)
                    annotate = __get_annotate_args(score_result_field)

                    annotate_args[annotate[0]] = annotate[1]
                    good_fields.append(score_result_field)

        """
        The filter function will grab score results for all teams requested, exclusively
        all that will be passed on to the page is the teams and fields asked for.
        """
        search_results = Team.objects.filter(teamNumber__in=teams).annotate(**annotate_args)
        context['results'] = __create_filtered_team_metrics(search_results, good_fields)

    return render(request, 'Scouting2016/showComparison.html', context)


def robot_display(request):

    """
    robot_display currently has no python implementation. It simply needs to load correctly
    as an HTML page, as it is just meant to show hard-coded information.
    """

    return render(request, 'Scouting2016/robot_info/overview.html')


def robot_display_software(request):

    """
    robot_display currently has no python implementation. It simply needs to load correctly
    as an HTML page, as it is just meant to show hard-coded information.
    """

    return render(request, 'Scouting2016/robot_info/software.html')


def robot_display_scaling(request):

    """
    robot_display currently has no python implementation. It simply needs to load correctly
    as an HTML page, as it is just meant to show hard-coded information.
    """

    return render(request, 'Scouting2016/robot_info/scaling.html')


def robot_display_overroller(request):

    """
    robot_display currently has no python implementation. It simply needs to load correctly
    as an HTML page, as it is just meant to show hard-coded information.
    """

    return render(request, 'Scouting2016/robot_info/overroller.html')


def robot_display_drivetrain(request):

    """
    robot_display currently has no python implementation. It simply needs to load correctly
    as an HTML page, as it is just meant to show hard-coded information.
    """

    return render(request, 'Scouting2016/robot_info/drivetrain.html')


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

    metrics = this_team.get_metrics()
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


def match_display(request, match_number):

    """
    This page will display any requested match. This page can be accessed through many places,
    such as the list of all matches, or when viewing any team's individual matches.
    @param match_number is the number of the match being displayed
    This page uses score results to show each team in the match, along with its statistics
    during just that match, not the overall average or sum as team in view_team
    """

    context = {}

    this_match = Match.objects.get(matchNumber=match_number)

    score_result_list = []

    for sr in this_match.scoreresult_set.all():
        score_result_list.append(sr)

    context['score_result_list'] = score_result_list
    context['match_display'] = match_number

    official_match_search = OfficialMatch.objects.filter(matchNumber=match_number)
    if len(official_match_search) == 1:
        official_match = official_match_search[0]
        valid, invalid_fields, = validate_match(this_match, official_match)
        if not valid:
            context['official_mismatch'] = invalid_fields

    return render(request, 'Scouting2016/MatchPage.html', context)


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

    context = {}
    context['match_number'] = match_number
    context['red_team_1'] = official_match.redTeam1
    context['red_team_2'] = official_match.redTeam2
    context['red_team_3'] = official_match.redTeam3
    context['blue_team_1'] = official_match.blueTeam1
    context['blue_team_2'] = official_match.blueTeam2
    context['blue_team_3'] = official_match.blueTeam3
    context['audience_defense'] = official_match.audienceSelectionCategory

    red_teams = [official_match.redTeam1, official_match.redTeam2, official_match.redTeam3]
    blue_teams = [official_match.blueTeam1, official_match.blueTeam2, official_match.blueTeam3]

    red_prediction, blue_prediction = official_match.predict_score()

    context['red_defenses'] = get_sorted_defense_stats(red_teams)
    context['blue_defenses'] = get_sorted_defense_stats(blue_teams)
    context['red_prediction'] = red_prediction
    context['blue_prediction'] = blue_prediction

    return render(request, 'Scouting2016/MatchPrediction.html', context)


def all_teams(request):

    """
    When requested, will show a list of all the teams that have been in a match,
    or will be in a match. This also shows some average scoring statistics of each team,
    so it is necessary to obtain their metrics data.
    """

    the_teams = Team.objects.all()

    teams_with_avg = []

    for team in the_teams:

        metrics = team.get_metrics()

        team_with_avg = {}
        team_with_avg["id"] = team.id
        team_with_avg["teamNumber"] = team.teamNumber
        team_with_avg["matches_scouted"] = team.scoreresult_set.count()
        team_with_avg["avgerages"] = metrics
        team_with_avg["bookmark"] = team.bookmark
        teams_with_avg.append(team_with_avg)
    context = {"teams": teams_with_avg}

    return render(request, 'Scouting2016/AllTeams.html', context)


def all_matches(request):

    """
    will show a list of all matches, both scouted already and unscouted (upcoming)
    Will show all teams in each match, and display them into two tables of each variety
    """

    matches = Match.objects.all()

    for match in matches:
        official_match_search = OfficialMatch.objects.filter(matchNumber=match.matchNumber)
        if len(official_match_search) == 1 and official_match_search[0].hasOfficialData:
            valid, _ = validate_match(match, official_match_search[0])
            match.validity = "Yes" if valid else "No"
        else:
            match.validity = "Unknown"

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


def upload_image(request):

    """
    Pictures can be uploaded from the users devices to the server and posts them to the team's
    respective team page
    """

    team_numer = request.POST['team_number']
    f = request.FILES['image_name']

    static_dir = 'ScoutingWebsite2015/Scouting2016/static/'
    out_file_name = static_dir + 'Scouting2016/robot_pics/%s_{0}%s' % (team_numer, os.path.splitext(f.name)[1])

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
    hack_test = "writing picture to %s, " % out_file_name
    hack_test += str(os.path.exists(out_file_name)) + ", "
    hack_test += str(os.path.abspath(out_file_name)) + ", " 
    #raise Exception(hack_test)
    with open(out_file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return HttpResponseRedirect(reverse('Scouting2016:view_team', args=(team_numer,)))

#######################################
# Form Stuff
#######################################


def showLogin(request):

    return render(request, 'Scouting2016/login.html')


def log_user_out(request):
    logout(request)

    return HttpResponseRedirect(reverse('Scouting2016:showLogin'))


def auth_login(request):
    username = request.POST['username']
    password = request.POST['password']
    good_redirect = request.POST.get('next', '/2016')
    bad_redirect = 'Scouting2016:showLogin'
    print good_redirect

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(good_redirect)
        else:
            return HttpResponseRedirect(reverse(bad_redirect))
    else:
        return HttpResponseRedirect(reverse(bad_redirect))


@permission_required('auth.can_modify_model', login_url=login_reverse)
def info_for_form_edit(request):

    return render(request, 'Scouting2016/info_for_form_edit.html')

@permission_required('auth.can_modify_model', login_url=login_reverse)
def show_add_form(request):

    context = {}
    context['team_number'] = 1
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

def submit_pit_scouting(request):
    
    return render(request, 'Scouting2016/inputForm.html')

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

    # Pit stuff


@permission_required('auth.can_modify_model', login_url=login_reverse)
def info_for_pit_edit(request):
    return render(request, 'Scouting2016/info_for_pit_edit.html')

@permission_required('auth.can_modify_model', login_url=login_reverse)
def show_add_pit(request):
    team =  request.GET["team_number"]
    print team;
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


def get_hovercard(request):
    context = {}
    type = request.GET.get('type')
    if type == "colSelectContent":
      return render(request, 'Scouting2016/hovercards/colSelectContent.html')
    elif type == "filterContent":
      context['filterType'] = request.GET.get('filterType')
      return render(request, 'Scouting2016/hovercards/filterContent.html', context)


def add_team_comments(request, team_number):
    comments = request.POST["team_comments"]
    team = Team.objects.get(teamNumber=team_number)
    teamComments = TeamComments.objects.create(team=team, comment=comments)
    print teamComments

    return HttpResponseRedirect(reverse('Scouting2016:view_team', args=(team_number,)))
def bookmark_team_page(request):
    team = Team.objects.get(teamNumber=request.POST['team_number'])
    team.bookmark = request.POST['bookmark']
    team.save()
    return HttpResponseRedirect(reverse('Scouting2016:view_team', args=(team.teamNumber,)))
