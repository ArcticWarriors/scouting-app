'''
Created on Jan 29, 2016

@author: PJ
'''

from Scouting2016.models import OfficialMatch, Match, Team
import random


def create_scoreresults():

    matches = Match.objects.all()

    for match in matches:

        kargs = {}
        kargs['matchNumber'] = match.matchNumber

        positions = ['redTeam1', 'redTeam2', 'redTeam3', 'blueTeam1', 'blueTeam2', 'blueTeam3']
        score_results = score_results = match.scoreresult_set.all()
        for i, sr in enumerate(score_results):
            team = sr.team
            kargs[positions[i]] = team.teamNumber

        OfficialMatch.objects.create(**kargs)


def create_unscouted_matches():
    teams = Team.objects.all()
    positions = ['redTeam1', 'redTeam2', 'redTeam3', 'blueTeam1', 'blueTeam2', 'blueTeam3']

#     for match_number in [21]:
    for match_number in range(41, 80, 1):
        kargs = {}
        kargs['matchNumber'] = match_number

        team_indices = []
        while len(team_indices) < 6:
            team_index = random.randint(0, len(teams) - 1)
            if team_index not in team_indices:
                team_indices.append(team_index)

        for i in range(len(team_indices)):
            kargs[positions[i]] = teams[team_indices[i]].teamNumber

        OfficialMatch.objects.create(**kargs)
