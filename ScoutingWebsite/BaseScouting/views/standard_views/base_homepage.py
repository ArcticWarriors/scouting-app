
from django.db.models import Q
from django.views.generic.base import TemplateView


class BaseHomepageView(TemplateView):
    def __init__(self, compition_model, team_model, match_model, official_match_model, template_name='BaseScouting/index.html'):
        self.compition_model = compition_model
        self.team_model = team_model
        self.match_model = match_model
        self.official_match_model = official_match_model

        self.template_name = template_name

    def get_context_data(self, **kwargs):
        competition = self.compition_model.objects.get(code=kwargs["regional_code"])

        context = super(BaseHomepageView, self).get_context_data(**kwargs)
        context['competition'] = competition
        context['our_metrics'] = self._get_our_metrics(competition)
        context['competition_metrics'] = self._get_competition_metrics(competition)
        context['our_next_match_prediction'] = self._get_next_match_prediction(competition)

        return context

    def _get_next_match_prediction(self, competition):

        our_team = self.team_model.objects.get(teamNumber=self._get_our_team_number())
        matches = self.match_model.objects.filter(competition=competition)
        matches = matches.filter(Q(red1=our_team) | Q(red2=our_team) | Q(red3=our_team) | Q(blue1=our_team) | Q(blue2=our_team) | Q(blue3=our_team))
        matches = sorted(matches, key=lambda match: match.matchNumber)

        official_matches = self.official_match_model.objects.filter(competition=competition, hasOfficialData=1)
        highest_official_match_search = official_matches.order_by('-matchNumber')
        highest_official_match_number = -1
        if len(highest_official_match_search) != 0:
            highest_official_match_number = highest_official_match_search[0].matchNumber
        print highest_official_match_number

        next_match = None
        for match in matches:
            if match.scoreresult_set.count() == 0 and match.matchNumber > highest_official_match_number:
                next_match = match
                break

        if next_match != None:
            return self._predict_match(next_match, competition)

        return None

    def _get_our_team_number(self):
        raise NotImplementedError("You need to implement the _get_our_team_number function!")

    def _get_our_metrics(self, competition):
        raise NotImplementedError("You need to implement the _get_our_metrics function!")

    def _get_competition_metrics(self, competition):
        raise NotImplementedError("You need to implement the _get_competition_metrics function!")

    def _predict_match(self, match, competition):
        raise NotImplementedError("You need to implement the _predict_match function!")
