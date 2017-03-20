from django.views.generic.base import TemplateView
import operator


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
        competes_in_query = sorted(competes_in_query, key=operator.attrgetter('team.teamNumber'))

        teams_with_metrics = []

        for competes_in in competes_in_query:
            team = competes_in.team
            team.metrics = self.get_metrics_for_team(team)
            teams_with_metrics.append(team)

        context = super(BaseTeamListView, self).get_context_data(**kwargs)
        context['teams'] = teams_with_metrics
        context['metric_fields'] = self.score_result_model.get_fields()
        return context
