'''
Created on Feb 22, 2017

@author: PJ
'''
from BaseScouting.views.forms.base_match_submission import BaseMatchEntryView
from Scouting2017.model.reusable_models import Match, TeamCompetesIn,\
    Competition
from Scouting2017.model.models2017 import ScoreResult


class MatchEntryView2017(BaseMatchEntryView):
    def __init__(self):
        BaseMatchEntryView.__init__(self, 'Scouting2017/match_entry.html')

    def has_scouted_info(self, team, match):

        return len(ScoreResult.objects.filter(team=team, match=match)) >= 1

    def get_context_data(self, **kwargs):
        context = super(BaseMatchEntryView, self).get_context_data(**kwargs)

        competition = Competition.objects.get(code=kwargs['regional_code'])
        matches = Match.objects.filter(competition=competition)

        match_to_scouted_teams = {}
        match_to_unscouted_teams = {}

        team_pair = TeamCompetesIn.objects.filter(competition=competition)
        context["teams"] = {pair.team.teamNumber: 0 for pair in team_pair}

        for match in matches:
            scouted = []
            unscouted = []

            self.__add_to_scouted_list(match, match.red1, scouted, unscouted)
            self.__add_to_scouted_list(match, match.red2, scouted, unscouted)
            self.__add_to_scouted_list(match, match.red3, scouted, unscouted)

            self.__add_to_scouted_list(match, match.blue1, scouted, unscouted)
            self.__add_to_scouted_list(match, match.blue2, scouted, unscouted)
            self.__add_to_scouted_list(match, match.blue3, scouted, unscouted)

            match_to_scouted_teams[match.matchNumber] = scouted
            match_to_unscouted_teams[match.matchNumber] = unscouted

        context["matches"] = {'scouted': match_to_scouted_teams, 'unscouted': match_to_unscouted_teams}

        return context

    def __add_to_scouted_list(self, match, team, out_scouted, out_unscouted):
        if self.has_scouted_info(team, match):
            out_scouted.append(team.teamNumber)
        else:
            out_unscouted.append(team.teamNumber)
