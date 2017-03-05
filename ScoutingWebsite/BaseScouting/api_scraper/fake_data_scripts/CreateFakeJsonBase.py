'''
Created on Mar 5, 2017

@author: PJ
'''
import random
import math
import collections


class CreateFakeJsonBase():

    def __init__(self, competition, match_model, official_match_model, official_match_sr_model):
        self.competition = competition
        self.match_model = match_model
        self.official_match_model = official_match_model
        self.official_match_sr_model = official_match_sr_model

        random.seed(100)

    def create_matches(self, min_match, max_match, robots):

        matches = []
        for match_num in range(min_match, max_match):

            match = self.match_model.objects.get(matchNumber=match_num, competition=self.competition)
            official_match = self.official_match_model.objects.get(matchNumber=match_num, competition=self.competition)
            official_match_srs = self.official_match_sr_model.objects.filter(official_match=official_match)

            if len(official_match_srs) == 2:
                matches.append(self._create_match(match, official_match_srs, robots))
                official_match.hasOfficialData = 1
                official_match.save()
            else:
                print "Official match isn't correct"

        return matches

    def _create_match(self, match, official_match_srs, robots):

        alliance_data = []

        red_teams = [match.red1, match.red2, match.red3]
        blue_teams = [match.blue1, match.blue2, match.blue3]

        alliances = collections.OrderedDict()
        alliances["Red"] = red_teams
        alliances["Blue"] = blue_teams

        for color, teams in alliances.items():
            team1sr = robots[teams[0].teamNumber].create_score_result()
            team2sr = robots[teams[1].teamNumber].create_score_result()
            team3sr = robots[teams[2].teamNumber].create_score_result()

            alliance_data.append(self._populateAlliance(color, [team1sr, team2sr, team3sr]))

        return self._prepare_match_info(official_match_srs[0].official_match.matchNumber, alliance_data, alliances)

    def _populateAlliance(self, teams):
        raise NotImplementedError()

    def _prepare_match_info(self, teams):
        raise NotImplementedError()
