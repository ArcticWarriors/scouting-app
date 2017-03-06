from django.views.generic.base import TemplateView
from django.db.models.aggregates import Avg
from django.db.models.expressions import Case, When
from Scouting2017.model.reusable_models import TeamCompetesIn, Team, Competition, \
    PickList
from Scouting2017.model.models2017 import ScoreResult
import operator
import json


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

        top_teams = {}

        averages = ScoreResult.objects.values("team_id").annotate(fuel=Avg("auto_fuel_high_score") + Avg("tele_fuel_high_score") / 3.0 + Avg("auto_fuel_low_score") / 3.0 + Avg("tele_fuel_low_score") / 9.0,
                                                                  gears=Avg("auto_gears") + Avg("tele_gears"),
                                                                  rope=Avg(Case(When(rope=True, then=1), When(rope=False, then=0)))
                                                                  ).order_by()

        gear_weight = 15
        category_size_to_add = 5

        sorted_overall = [Team.objects.get(id=x["team_id"]).teamNumber for x in sorted(averages, key=lambda x: x["fuel"] + x["gears"] * gear_weight + x["rope"], reverse=True)]

        top_fuel = [Team.objects.get(id=x["team_id"]).teamNumber for x in sorted(averages, key=lambda x: x["fuel"], reverse=True)[0:category_size_to_add]]
        top_gear = [Team.objects.get(id=x["team_id"]).teamNumber for x in sorted(averages, key=lambda x: x["gears"], reverse=True)[0:category_size_to_add]]
        top_teams["fuel"] = top_fuel
        top_teams["gear"] = top_gear
        top_teams["overall"] = sorted_overall[:24]
        top_teams["do_not_pick"] = sorted_overall[-category_size_to_add:]
        top_teams["defense"] = sorted_overall[-category_size_to_add:]

        context["top_teams"] = top_teams

        return context
