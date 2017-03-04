from django.views.generic.base import TemplateView
from Scouting2017.model.reusable_models import TeamCompetesIn, Team, Competition, \
    PickList
import operator


class PickListView2017(TemplateView):
    def __init__(self):
        self.template_name = 'Scouting2017/pick_list.html'

    def get_context_data(self, **kwargs):
        context = super(PickListView2017, self).get_context_data(**kwargs)

        all_teams = []
        competition = Competition.objects.get(code=kwargs['regional_code'])
        for team_competes_in in TeamCompetesIn.objects.filter(competition=competition):
            all_teams.append(team_competes_in.team)

        all_teams = sorted(all_teams, key=operator.attrgetter('teamNumber'))

        context['original_overall_list'] = PickList.objects.filter(competition=competition, grouping="Overall").order_by('rank_in_group')
        context['original_fuel_list'] = PickList.objects.filter(competition=competition, grouping="Fuel").order_by('rank_in_group')
        context['original_gear_list'] = PickList.objects.filter(competition=competition, grouping="Gear").order_by('rank_in_group')
        context['original_defense_list'] = PickList.objects.filter(competition=competition, grouping="Defense").order_by('rank_in_group')
        context['original_dnp_list'] = PickList.objects.filter(competition=competition, grouping="Do Not Pick").order_by('rank_in_group')
        context['all_teams'] = all_teams

        return context
