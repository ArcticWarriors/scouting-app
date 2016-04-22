'''
Created on Apr 21, 2016

@author: PJ
'''
import os
import json
from django.db import transaction


class PopulateRegionalresults:

    def __init__(self, team_model, competition_model, official_match_model, official_match_sr_model):
        self.team_model = team_model
        self.competition_model = competition_model
        self.official_match_model = official_match_model
        self.official_match_sr_model = official_match_sr_model

    def read_local_copy(self, input_file):
        with open(input_file, 'r') as f:
            response_body = f.read()

        json_struct = json.loads(response_body)

        return json_struct

    @transaction.atomic
    def update_team_info(self, event_code, json_path):

        local_file = json_path + '/{0}_team_query.json'.format(event_code)
        if not os.path.exists(local_file):
            print "No team info, skipping population"
            return

        json_struct = self.read_local_copy(local_file)

        for team_info in json_struct["teams"]:
            team_number = team_info["teamNumber"]

            team, _ = self.team_model.objects.get_or_create(teamNumber=team_number)
            team.teamHomepage = team_info["website"] if team_info["website"] != None else "NA"
            team.teamFirstYear = team_info["rookieYear"]
            team.save()
            print "Updating info for team %s" % team_number

    @transaction.atomic
    def update_schedule(self, event_code, json_path):

        competition = self.competition_model.objects.get(code=event_code)

        local_file = json_path + '/{0}_schedule_query.json'.format(event_code)
        if not os.path.exists(local_file):
            print "No schedule info, skipping population"
            return

        json_struct = self.read_local_copy(local_file)

        schedule_info = json_struct["Schedule"]

        for match_info in schedule_info:
            match_number = match_info["matchNumber"]

            red_teams = []
            blue_teams = []

            for team_info in match_info["Teams"]:
                team, _ = self.team_model.objects.get_or_create(teamNumber=team_info["teamNumber"])
                if "Red" in team_info["station"]:
                    red_teams.append(team)
                elif "Blue" in team_info["station"]:
                    blue_teams.append(team)

            official_match, _ = self.official_match_model.objects.get_or_create(matchNumber=match_number, competition=competition)
            match_sr_search = self.official_match_sr_model.objects.filter(official_match=official_match)

            if len(match_sr_search) == 2:
                print "Updating teams for match %s" % official_match.matchNumber
            elif len(match_sr_search) == 0:
                self.official_match_sr_model.objects.create(official_match=official_match, competition=competition, team1=red_teams[0], team2=red_teams[1], team3=red_teams[2],)
                self.official_match_sr_model.objects.create(official_match=official_match, competition=competition, team1=blue_teams[0], team2=blue_teams[1], team3=blue_teams[2],)
                print "Creating official match %s" % official_match.matchNumber
            else:
                print "UH OH"

    @transaction.atomic
    def update_matchresults(self, event_code, json_path):
        competition = self.competition_model.objects.get(code=event_code)

        local_file = json_path + '/{0}_scoreresult_query.json'.format(event_code)
        if not os.path.exists(local_file):
            print "No official results, skipping population"
            return

        json_struct = self.read_local_copy(local_file)

        scores_info = json_struct["MatchScores"]
        for match_info in scores_info:
            match_number = match_info["matchNumber"]

            for alliance_info in match_info["Alliances"]:
                official_match = self.official_match_model.objects.get(matchNumber=match_number, competition=competition)
                official_sr_search = self.official_match_sr_model.objects.filter(official_match=official_match)
                if len(official_sr_search) != 2:
                    print "Uh oh..."
                    continue

                color = alliance_info["alliance"]
                if color == "Red":
                    self.populate_official_sr(official_sr_search[0], alliance_info)

                if color == "Blue":
                    self.populate_official_sr(official_sr_search[1], alliance_info)

            print "Adding stats to official match %s" % official_match.matchNumber

    def populate_official_sr(self, official_match_sr, alliance_info):
        raise NotImplementedError()
