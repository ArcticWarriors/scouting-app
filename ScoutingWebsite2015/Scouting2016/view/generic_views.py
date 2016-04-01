'''
Created on Mar 28, 2016

@author: PJ
'''

from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from Scouting2016.model.reusable_models import Team, Match, OfficialMatch, \
    TeamPictures, TeamComments


class AllTeamsViews(TemplateView):
    """
    When requested, will show a list of all the teams that have been in a match,
    or will be in a match. This also shows some average scoring statistics of each team,
    so it is necessary to obtain their metrics data.
    """

    template_name = 'Scouting2016/all_teams.html'

    def get_context_data(self, **kwargs):
        all_teams = Team.objects.all()

        teams_with_metrics = []

        for team in all_teams:
            team.metrics = self.get_metrics_for_team(team)
            teams_with_metrics.append(team)

        context = super(AllTeamsViews, self).get_context_data(**kwargs)
        context['teams'] = teams_with_metrics

        return context


class SingleTeamView(TemplateView):

    template_name = 'Scouting2016/view_team.html'

    def get_context_data(self, **kwargs):

        team = get_object_or_404(Team, teamNumber=kwargs["team_number"])

        score_results = [sr for sr in team.scoreresult_set.all()]

        context = super(SingleTeamView, self).get_context_data(**kwargs)
        context['team'] = team
        context['score_result_list'] = score_results
        context['pictures'] = TeamPictures.objects.filter(team_id=team.id)
        context['team_comments'] = TeamComments.objects.filter(team=team)
        context['metrics'] = self.get_metrics(team)

        print context['team_comments']

        return context


class AllMatchesView(TemplateView):

    template_name = 'Scouting2016/all_matches.html'

    def get_context_data(self, **kwargs):
        matches = Match.objects.all()
        scouted_numbers = [match.matchNumber for match in matches]
        unscouted_matches = OfficialMatch.objects.all().exclude(matchNumber__in=scouted_numbers)

        context = super(AllMatchesView, self).get_context_data(**kwargs)
        context['scouted_matches'] = matches
        context['unscouted_matches'] = unscouted_matches

        return context


class SingleMatchView(TemplateView):
    """
    This page will display any requested match. This page can be accessed through many places,
    such as the list of all matches, or when viewing any team's individual matches.
    @param match_number is the number of the match being displayed
    This page uses score results to show each team in the match, along with its statistics
    during just that match, not the overall average or sum as team in view_team
    """

    template_name = 'Scouting2016/view_match.html'

    def get_context_data(self, **kwargs):
        the_match = get_object_or_404(Match, matchNumber=kwargs["match_number"])

        context = super(SingleMatchView, self).get_context_data(**kwargs)
        context['match'] = the_match

        return context


class OfficialMatchView(TemplateView):
    """
    This page is displayed when a match which has not happened yet would be requested
    the page is useful for upcoming matches, as it can display which defenses each ALLIANCE
    crosses the most and the least (ecxluding the low bar, since it will always be on the field
    and is irrelevant for our purposes) by obtaining information from get_defnese_stats, and addimg
    the total crosses from each team into a grand total. This total is then sorted into a ranked
    list by using the sorted() function with reverse=true.
    @param match_number is the match which is being predicted.
    """

    template_name = 'Scouting2016/view_official_match.html'

    def get_context_data(self, **kwargs):

        official_match = get_object_or_404(OfficialMatch, matchNumber=kwargs["match_number"])

        context = super(OfficialMatchView, self).get_context_data(**kwargs)
        context['match_number'] = official_match.matchNumber
        context['results'] = self.get_score_results(official_match)
        print context

        return context
