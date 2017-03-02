from BaseScouting.views.base_views import BaseSingleTeamView
from Scouting2017.model.reusable_models import Team, TeamPictures, TeamComments
from Scouting2017.model.models2017 import TeamPitScouting, get_team_metrics


class SingleTeamView2017(BaseSingleTeamView):

    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, 'Scouting2017/team.html')

    def get_context_data(self, **kwargs):
        context = BaseSingleTeamView.get_context_data(self, **kwargs)

        if context['metrics']['tele_fuel_high_score__avg'] != "NA":

            context['metrics']['tele_fuel_high_misses__avg'] = float(context['metrics']['tele_fuel_high_shots__avg']) - float(context['metrics']['tele_fuel_high_score__avg'])
            context['metrics']['auto_fuel_high_misses__avg'] = float(context['metrics']['auto_fuel_high_shots__avg']) - float(context['metrics']['auto_fuel_high_score__avg'])
            context['metrics']['tele_fuel_low_misses__avg'] = float(context['metrics']['tele_fuel_low_shots__avg']) - float(context['metrics']['tele_fuel_low_score__avg'])
            context['metrics']['auto_fuel_low_misses__avg'] = float(context['metrics']['auto_fuel_low_shots__avg']) - float(context['metrics']['auto_fuel_low_score__avg'])
#             context['metrics']['fuel_shot_hi_missed_auto__avg'] = float(context['metrics']['fuel_shot_hi_auto__avg']) - float(context['metrics']['fuel_score_hi_auto__avg'])
#             context['metrics']['fuel_shot_low_missed__avg'] = float(context['metrics']['fuel_shot_low__avg']) - float(context['metrics']['fuel_score_low__avg'])
#             context['metrics']['fuel_shot_low_missed_auto__avg'] = float(context['metrics']['fuel_shot_low_auto__avg']) - float(context['metrics']['fuel_score_low_auto__avg'])
        else:
            context['metrics']['tele_fuel_high_misses__avg'] = "NA"
            context['metrics']['auto_fuel_high_misses__avg'] = "NA"
            context['metrics']['fuel_shot_low_missed__avg'] = "NA"
            context['metrics']['fuel_shot_low_missed_auto__avg'] = "NA"

        pit_scouting_search = TeamPitScouting.objects.filter(team__teamNumber=kwargs["team_number"])
        if len(pit_scouting_search) == 1:
            context['pit_scouting'] = pit_scouting_search[0]

        return context

    def get_metrics(self, team):
        return get_team_metrics(team)
