from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
import operator


class BaseSingleMatchView(TemplateView):
    """
    This page will display any requested match. This page can be accessed through many places,
    such as the list of all matches, or when viewing any team's individual matches.
    @param match_number is the number of the match being displayed
    This page uses score results to show each team in the match, along with its statistics
    during just that match, not the overall average or sum as team in view_team
    """

    def __init__(self, year, match_model, template_name):
        self.match_model = match_model
        self.template_name = template_name
        self.year = year

    def get_context_data(self, **kwargs):
        the_match = get_object_or_404(self.match_model, matchNumber=kwargs["match_number"], competition__code=kwargs["regional_code"])

        context = super(BaseSingleMatchView, self).get_context_data(**kwargs)
        context['match'] = the_match

        score_results = []
        for sr in the_match.scoreresult_set.all():
            if sr.team == the_match.red1 or sr.team == the_match.red2 or sr.team == the_match.red3:
                sr.color = "Red"
            elif sr.team == the_match.blue1 or sr.team == the_match.blue2 or sr.team == the_match.blue3:
                sr.color = "Blue"
            else:
                sr.color = "Error"
            score_results.append(sr)

        score_results.sort(key=operator.attrgetter('color'), reverse=True)

        has_official_data, warnings, errors = self.get_match_validation(kwargs["regional_code"], the_match)
        context['official_result_warnings'] = warnings
        context['official_result_errors'] = errors
        context['has_official_data'] = has_official_data
        context['score_result_list'] = score_results
        context['tba_code'] = self._get_tba_event_code(kwargs["regional_code"])

        metrics = []
        for sr in the_match.scoreresult_set.all():
            metrics.append(self.get_metrics(sr))
        context['metrics'] = metrics

        return context

    def _get_tba_event_code(self, competition_code):
        return "%s%s" % (self.year, competition_code.lower())

    def get_match_validation(self, regional_code, match):
        raise NotImplementedError("You need to implement the get_match_validation function")

