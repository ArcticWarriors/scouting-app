from django.views.generic.base import TemplateView
import operator


class BaseMatchListView(TemplateView):

    def __init__(self, year, match_model, template_name='BaseScouting/match_list.html'):
        self.match_model = match_model
        self.template_name = template_name
        self.year = year

    def get_context_data(self, **kwargs):
        matches = self.match_model.objects.filter(competition__code=kwargs["regional_code"])
        matches = sorted(matches, key=operator.attrgetter('matchNumber'))

        scouted_matches = []
        unscouted_matches = []

        for match in matches:
            srs = match.scoreresult_set.all()
            if len(srs) == 0:
                unscouted_matches.append(self._append_unscouted_info(match, kwargs["regional_code"]))
            else:
                scouted_matches.append(self._append_scouted_info(match, kwargs["regional_code"]))

        context = super(BaseMatchListView, self).get_context_data(**kwargs)
        context['scouted_matches'] = scouted_matches
        context['unscouted_matches'] = unscouted_matches
        context['tba_code'] = self._get_tba_event_code(kwargs["regional_code"])

        return context

    def _get_tba_event_code(self, competition_code):
        return "%s%s" % (self.year, competition_code.lower())

    def _append_scouted_info(self, match, regional_code):
        raise NotImplementedError("You need to implement the _append_scouted_info function")

    def _append_unscouted_info(self, match, regional_code):
        raise NotImplementedError("You need to implement the _append_unscouted_info function")

