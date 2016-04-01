import operator

from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models.aggregates import Avg, Sum
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from Scouting2016.models import Team, Match, ScoreResult, TeamPictures, OfficialMatch, TeamComments
from django.contrib.auth.decorators import permission_required
from Scouting2016.model.models2016 import get_team_metrics, get_defense_stats
from Scouting2016.view.generic_views import SingleTeamView, SingleMatchView, \
    OfficialMatchView, AllTeamsViews, AddTeamPictureView


login_reverse = reverse_lazy('Scouting2016:showLogin')


class AllTeamsViews2016(AllTeamsViews):

    def get_metrics_for_team(self, team):
        return get_team_metrics(team)


class AddTeamPictureView2016(AddTeamPictureView):

    def __init__(self):
        AddTeamPictureView.__init__(self, 'Scouting2016/static', 'Scouting2016/robot_pics')


class SingleTeamView2016(SingleTeamView):

    def get_metrics(self, team):
        return get_team_metrics(team)


class SingleMatchView2016(SingleMatchView):
    pass


class OfficialMatchView2016(OfficialMatchView):

    def __get_sorted_defense_stats(self, official_score_result):
        results = {}

        get_defense_stats(official_score_result.team1, results)
        get_defense_stats(official_score_result.team2, results)
        get_defense_stats(official_score_result.team3, results)

        for category in results:
            results[category] = sorted(results[category].items(), key=operator.itemgetter(1), reverse=True)

        return sorted(results.items())

    def get_score_results(self, official_match):

        results = official_match.officialmatchscoreresult_set.all()
        blue_results = results[0]
        red_results = results[1]

        output = {}
        output['red_results'] = red_results
        output['blue_results'] = blue_results

        output['red_defenses'] = self.__get_sorted_defense_stats(red_results)
        output['blue_defenses'] = self.__get_sorted_defense_stats(blue_results)

        return output


# def get_sorted_defense_stats(teams):
#     results = {}
#
#     for team in teams:
#         team.get_defense_stats(results)
#
#     for category in results:
#         results[category] = sorted(results[category].items(), key=operator.itemgetter(1), reverse=True)
#
#     return sorted(results.items())
#
#
# def match_prediction(request, match_number):
#
#     """
#     This page is displayed when a match which has not happened yet would be requested
#     the page is useful for upcoming matches, as it can display which defenses each ALLIANCE
#     crosses the most and the least (ecxluding the low bar, since it will always be on the field
#     and is irrelevant for our purposes) by obtaining information from get_defnese_stats, and addimg
#     the total crosses from each team into a grand total. This total is then sorted into a ranked
#     list by using the sorted() function with reverse=true.
#     @param match_number is the match which is being predicted.
#     """
#
#     official_match = OfficialMatch.objects.get(matchNumber=match_number)
#     score_results = official_match.officialmatchscoreresult_set.all()
#     red_results = score_results[0]
#     blue_results = score_results[1]
#
#     context = {}
#     context['match_number'] = match_number
#     context['red_results'] = red_results
#     context['blue_results'] = blue_results
# #     context['audience_defense'] = official_match.audienceSelectionCategory
#
# #     red_teams = [official_match.redTeam1, official_match.redTeam2, official_match.redTeam3]
# #     blue_teams = [official_match.blueTeam1, official_match.blueTeam2, official_match.blueTeam3]
# #
# #     red_prediction, blue_prediction = official_match.predict_score()
# #
# #     context['red_defenses'] = get_sorted_defense_stats(red_teams)
# #     context['blue_defenses'] = get_sorted_defense_stats(blue_teams)
# #     context['red_prediction'] = red_prediction
# #     context['blue_prediction'] = blue_prediction
#
#     return render(request, 'Scouting2016/view_official_match.html', context)
#
#
#
# def get_hovercard(request):
#     context = {}
#     the_type = request.GET.get('type')
#     if the_type == "colSelectContent":
#         return render(request, 'Scouting2016/hovercards/colSelectContent.html')
#     elif the_type == "filterContent":
#         context['filterType'] = request.GET.get('filterType')
#         return render(request, 'Scouting2016/hovercards/filterContent.html', context)
