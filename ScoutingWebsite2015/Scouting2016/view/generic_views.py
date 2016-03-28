'''
Created on Mar 28, 2016

@author: PJ
'''

import os
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from Scouting2016.model.reusable_models import Team, Match, OfficialMatch, \
    TeamPictures, TeamComments


def index(request):

    return render(request, 'Scouting2016/index.html')


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

    return response


def robot_display(request):

    """
    robot_display currently has no python implementation. It simply needs to load correctly
    as an HTML page, as it is just meant to show hard-coded information.
    """

    return render(request, 'Scouting2016/robot_info/overview.html')


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
    if len(official_match_search) == 1 and official_match_search[0].hasOfficialData:
        context['has_official_data'] = True
        official_match = official_match_search[0]
#         valid, invalid_fields, = validate_match(this_match, official_match)
#         if not valid:
#             context['official_mismatch'] = invalid_fields
    else:
        context['has_official_data'] = False

    return render(request, 'Scouting2016/MatchPage.html', context)


def all_teams(request):

    """
    When requested, will show a list of all the teams that have been in a match,
    or will be in a match. This also shows some average scoring statistics of each team,
    so it is necessary to obtain their metrics data.
    """

    the_teams = Team.objects.all()

    teams_with_avg = []

    for team in the_teams:

#         metrics = team.get_metrics()

        team_with_avg = {}
        team_with_avg["id"] = team.id
        team_with_avg["teamNumber"] = team.teamNumber
        team_with_avg["matches_scouted"] = team.scoreresult_set.count()
#         team_with_avg["avgerages"] = metrics
        team_with_avg["bookmark"] = team.teampitscouting.bookmark
        teams_with_avg.append(team_with_avg)
    context = {"teams": teams_with_avg}

    return render(request, 'Scouting2016/AllTeams.html', context)


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
    with open(out_file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return HttpResponseRedirect(reverse('Scouting2016:view_team', args=(team_numer,)))


def all_matches(request):

    """
    will show a list of all matches, both scouted already and unscouted (upcoming)
    Will show all teams in each match, and display them into two tables of each variety
    """

    matches = Match.objects.all()

#     for match in matches:
#         official_match_search = OfficialMatch.objects.filter(matchNumber=match.matchNumber)
#         if len(official_match_search) == 1 and official_match_search[0].hasOfficialData:
#             valid, _ = validate_match(match, official_match_search[0])
#             match.validity = "Yes" if valid else "No"
#         else:
#             match.validity = "Unknown"

    scouted_numbers = [match.matchNumber for match in matches]
    unscouted_matches = OfficialMatch.objects.all().exclude(matchNumber__in=scouted_numbers)

    context = {}
    context['scouted_matches'] = matches
    context['unscouted_matches'] = unscouted_matches

    return render(request, 'Scouting2016/AllMatches.html', context)


def add_team_comments(request, team_number):
    comments = request.POST["team_comments"]
    team = Team.objects.get(teamNumber=team_number)
    teamComments = TeamComments.objects.create(team=team, comment=comments)
    print teamComments

    return HttpResponseRedirect(reverse('Scouting2016:view_team', args=(team_number,)))
