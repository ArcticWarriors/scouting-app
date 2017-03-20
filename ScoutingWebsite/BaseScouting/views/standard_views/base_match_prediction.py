from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404


class BaseMatchPredictionView(TemplateView):
    """
    This page is displayed when a match which has not happened yet would be requested
    the page is useful for upcoming matches, as it can display which defenses each ALLIANCE
    crosses the most and the least (ecxluding the low bar, since it will always be on the field
    and is irrelevant for our purposes) by obtaining information from get_defnese_stats, and addimg
    the total crosses from each team into a grand total. This total is then sorted into a ranked
    list by using the sorted() function with reverse=true.
    @param match_number is the match which is being predicted.
    """

    def __init__(self, match_model, competition_model, template_name):
        self.match_model = match_model
        self.competition_model = competition_model
        self.template_name = template_name

    def get_context_data(self, **kwargs):

        competition = self.competition_model.objects.get(code=kwargs["regional_code"])
        match = get_object_or_404(self.match_model, matchNumber=kwargs["match_number"], competition=competition)

        context = super(BaseMatchPredictionView, self).get_context_data(**kwargs)
        context['match_number'] = match.matchNumber
        context['predicted_results'] = self.get_score_results(match, competition)

        return context

    def get_score_results(self, match, competition):
        raise NotImplementedError()

