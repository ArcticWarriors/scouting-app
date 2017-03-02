from django.views.generic.base import TemplateView
from Scouting2017.model.reusable_models import TeamCompetesIn, Team
import operator


class PickListView2017(TemplateView):
    def __init__(self):
        self.template_name = 'Scouting2017/pick_list.html'

    def get_context_data(self, **kwargs):
        context = super(PickListView2017, self).get_context_data(**kwargs)

        all_teams = []
        for team_competes_in in TeamCompetesIn.objects.filter(competition__code=kwargs['regional_code']):
            all_teams.append(team_competes_in.team)

        all_teams = sorted(all_teams, key=operator.attrgetter('teamNumber'))

        context['original_overall_list'] = []
        context['original_fuel_list'] = []
        context['original_gear_list'] = []
        context['original_defense_list'] = []
        context['original_dnp_list'] = []
        context['all_teams'] = all_teams

        for i, team in enumerate(Team.objects.all()):

            if i < 24:
                context['original_overall_list'].append(team)
                context['original_fuel_list'].append(team)
                context['original_gear_list'].append(team)
                context['original_defense_list'].append(team)
            elif i < 30:
                context['original_dnp_list'].append(team)

        return context
