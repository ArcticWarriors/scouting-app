'''
Created on Apr 26, 2016

@author: PJ
'''

import os
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateView, View
from django.shortcuts import get_object_or_404


class BaseHomepageView(TemplateView):
    def __init__(self, compition_model, template_name='BaseScouting/index.html'):
        self.compition_model = compition_model

        self.template_name = template_name

    def get_context_data(self, **kwargs):
        competition = self.compition_model.objects.get(code=kwargs["regional_code"])

        context = super(BaseHomepageView, self).get_context_data(**kwargs)
        context['competition'] = competition
        context['our_metrics'] = self.get_our_metrics()
        context['competition_metrics'] = self.get_competition_metrics(competition)

        return context


class BaseAddTeamCommentsView(View):

    def __init__(self, team_model, team_comments_model, reverse_name):
        self.team_model = team_model
        self.team_comments_model = team_comments_model
        self.reverse_name = reverse_name

    def post(self, request, team_number):
        comments = request.POST["team_comments"]
        team = self.team_model.objects.get(teamNumber=team_number)
        self.team_comments_model.objects.create(team=team, comment=comments)

        return HttpResponseRedirect(reverse(self.reverse_name, args=(team_number,)))


class BaseAddTeamPictureView(View):

    def __init__(self, team_model, team_pictures_model, static_dir, picture_location, reverse_name):
        self.team_model = team_model
        self.team_pictures_model = team_pictures_model

        self.static_dir = static_dir
        self.picture_location = picture_location
        self.reverse_name = reverse_name

    def post(self, request, **kargs):

        """
        Pictures can be uploaded from the users devices to the server and posts them to the team's
        respective team page
        """

        regional_code = kargs['regional_code']
        team_numer = request.POST['team_number']
        f = request.FILES['image_name']

        out_file_name = os.path.join(self.static_dir, self.picture_location) + "/" + ('%s_{0}%s' % (team_numer, os.path.splitext(f.name)[1]))

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

        database_name = out_file_name[len(self.static_dir) + 1:]

        team = self.team_model.objects.get(teamNumber=team_numer)
        self.team_pictures_model.objects.create(team=team, path=database_name)

        # Write the file to disk
        with open(out_file_name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        return HttpResponseRedirect(reverse(self.reverse_name, args=(regional_code, team_numer,)))


class BaseTeamListView(TemplateView):
    """
    When requested, will show a list of all the teams that have been in a match,
    or will be in a match. This also shows some average scoring statistics of each team,
    so it is necessary to obtain their metrics data.
    """

    def __init__(self, team_competes_in_model, score_result_model, template_name='BaseScouting/team_list.html'):
        self.team_competes_in_model = team_competes_in_model
        self.score_result_model = score_result_model
        self.template_name = template_name

    def get_context_data(self, **kwargs):
        competes_in_query = self.team_competes_in_model.objects.filter(competition__code=kwargs["regional_code"])

        teams_with_metrics = []

        for competes_in in competes_in_query:
            team = competes_in.team
            team.metrics = self.get_metrics_for_team(team)
            teams_with_metrics.append(team)
        
        context = super(BaseTeamListView, self).get_context_data(**kwargs)
        context['teams'] = teams_with_metrics
        context['metric_fields'] = self.score_result_model.get_fields()
        return context

# TODO: Remove once Scouting2017 can be refactored
class BaseAllTeamsViews(TemplateView):
    def __init__(self, team_competesin_model, template_name):
        self.team_competesin_model = team_competesin_model
        self.template_name = template_name

    def get_context_data(self, **kwargs):
        competes_in_query = self.team_competesin_model.objects.filter(competition__code=kwargs["regional_code"])

        teams_with_metrics = []

        for competes_in in competes_in_query:
            team = competes_in.team
            team.metrics = self.get_metrics_for_team(team)
            teams_with_metrics.append(team)

        context = super(BaseAllTeamsViews, self).get_context_data(**kwargs)
        context['teams'] = teams_with_metrics

        return context
    
class BaseSingleTeamView(TemplateView):

    def __init__(self, team_model, team_pictures_model, team_comments_model, template_name):
        self.team_model = team_model
        self.team_pictures_model = team_pictures_model
        self.team_comments_model = team_comments_model
        self.template_name = template_name

    def get_context_data(self, **kwargs):

        team = get_object_or_404(self.team_model, teamNumber=kwargs["team_number"])

        score_results = [sr for sr in team.scoreresult_set.all()]

        context = super(BaseSingleTeamView, self).get_context_data(**kwargs)
        context['team'] = team
        context['score_result_list'] = score_results
        context['pictures'] = self.team_pictures_model.objects.filter(team_id=team.id)
        context['team_comments'] = self.team_comments_model.objects.filter(team=team)
        context['metrics'] = self.get_metrics(team)

        return context


class BaseMatchListView(TemplateView):

    def __init__(self, match_model, official_match_model, template_name='BaseScouting/match_list.html'):
        self.match_model = match_model
        self.official_match_model = official_match_model
        self.template_name = template_name

    def get_context_data(self, **kwargs):
        matches = self.match_model.objects.filter(competition__code=kwargs["regional_code"])
        scouted_numbers = [match.matchNumber for match in matches]
        unscouted_matches = self.official_match_model.objects.filter(competition__code=kwargs["regional_code"]).exclude(matchNumber__in=scouted_numbers)

        context = super(BaseMatchListView, self).get_context_data(**kwargs)
        context['scouted_matches'] = matches
        context['unscouted_matches'] = unscouted_matches

        return context

# TODO: Remove once Scouting2017 can be refactored
class BaseAllMatchesView(BaseMatchListView):
    pass

class BaseSingleMatchView(TemplateView):
    """
    This page will display any requested match. This page can be accessed through many places,
    such as the list of all matches, or when viewing any team's individual matches.
    @param match_number is the number of the match being displayed
    This page uses score results to show each team in the match, along with its statistics
    during just that match, not the overall average or sum as team in view_team
    """

    def __init__(self, match_model, template_name):
        self.match_model = match_model
        self.template_name = template_name

    def get_context_data(self, **kwargs):
        the_match = get_object_or_404(self.match_model, matchNumber=kwargs["match_number"])

        context = super(BaseSingleMatchView, self).get_context_data(**kwargs)
        context['match'] = the_match
        context['score_result_list'] = [sr for sr in the_match.scoreresult_set.all()]

        metrics = []
        for sr in the_match.scoreresult_set.all():
            metrics.append(self.get_metrics(sr))
        context['metrics'] = metrics

        return context


class BaseOfficialMatchView(TemplateView):
    """
    This page is displayed when a match which has not happened yet would be requested
    the page is useful for upcoming matches, as it can display which defenses each ALLIANCE
    crosses the most and the least (ecxluding the low bar, since it will always be on the field
    and is irrelevant for our purposes) by obtaining information from get_defnese_stats, and addimg
    the total crosses from each team into a grand total. This total is then sorted into a ranked
    list by using the sorted() function with reverse=true.
    @param match_number is the match which is being predicted.
    """

    def __init__(self, official_match_model, template_name):
        self.official_match_model = official_match_model
        self.template_name = template_name

    def get_context_data(self, **kwargs):

        official_match = get_object_or_404(self.official_match_model, matchNumber=kwargs["match_number"])

        context = super(BaseOfficialMatchView, self).get_context_data(**kwargs)
        context['match_number'] = official_match.matchNumber
        context['results'] = self.get_score_results(official_match)

        return context


class BaseGenGraphView(View):

    def __init__(self, team_model):
        self.team_model = team_model

    def get(self, request, **kwargs):

        fields = kwargs['fields']
        team_numbers = kwargs['team_numbers']

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
            team = self.team_model.objects.get(teamNumber=int(team_number))

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
