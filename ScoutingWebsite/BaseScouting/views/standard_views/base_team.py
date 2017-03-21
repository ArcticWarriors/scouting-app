from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import Q


class BaseSingleTeamView(TemplateView):

    def __init__(self, team_model, team_pictures_model, team_comments_model, team_pit_scouting_model, team_competes_in_model, template_name):
        self.team_model = team_model
        self.team_pictures_model = team_pictures_model
        self.team_comments_model = team_comments_model
        self.team_pit_scouting_model = team_pit_scouting_model
        self.team_competes_in_model = team_competes_in_model
        self.template_name = template_name

    def get_context_data(self, **kwargs):

        team = get_object_or_404(self.team_model, teamNumber=kwargs["team_number"])

        score_results = [sr for sr in team.scoreresult_set.filter(competition__code=kwargs["regional_code"])]

        context = super(BaseSingleTeamView, self).get_context_data(**kwargs)
        context['team'] = team
        context['score_result_list'] = score_results
        context['pictures'] = self.team_pictures_model.objects.filter(team_id=team.id)
        context['team_comments'] = self.team_comments_model.objects.filter(team=team)
        context['metrics'] = self._get_metrics(team, kwargs["regional_code"])
        context['other_competitions'] = [pair.competition for pair in self.team_competes_in_model.objects.filter(~Q(competition__code=kwargs["regional_code"]) & Q(team=team))]

        pit_scouting_search = self.team_pit_scouting_model.objects.filter(team__teamNumber=kwargs["team_number"])
        if len(pit_scouting_search) == 1:
            context['pit_scouting'] = pit_scouting_search[0]

        return context

    def _get_metrics(self, team, regional_code):
        raise NotImplementedError("You need to implement the _get_metrics function!")
