'''
Created on Apr 21, 2016

@author: PJ
'''
import os
import json
from django.db import transaction


class PopulateRegionalResults:

    def __init__(self, team_model, team_competes_in_model, match_model, competition_model, official_match_model, official_match_sr_model):
        self.team_model = team_model
        self.team_competes_in_model = team_competes_in_model
        self.match_model = match_model
        self.competition_model = competition_model
        self.official_match_model = official_match_model
        self.official_match_sr_model = official_match_sr_model

    def __read_local_copy(self, input_file):
        with open(input_file, 'r') as f:
            response_body = f.read()

        json_struct = json.loads(response_body)

        return json_struct

    def __get_non_null_field(self, team_info, field_name, default="Unknown"):

        return team_info[field_name] if team_info[field_name] != None else default

    def __update_team_info(self, local_file):

        if not os.path.exists(local_file):
            print("No team info, skipping population")
            return

        json_struct = self.__read_local_copy(local_file)

        for team_info in json_struct["teams"]:
            team_number = team_info["teamNumber"]

            team, _ = self.team_model.objects.get_or_create(teamNumber=team_number)
            team.homepage = self.__get_non_null_field(team_info, "website")
            team.rookie_year = self.__get_non_null_field(team_info, "rookieYear")
            team.city = self.__get_non_null_field(team_info, "city")
            team.state = self.__get_non_null_field(team_info, "stateProv")
            team.country = self.__get_non_null_field(team_info, "country")
            team.team_name = self.__get_non_null_field(team_info, "nameFull")
            team.team_nickname = self.__get_non_null_field(team_info, "nameShort")
            team.robot_name = self.__get_non_null_field(team_info, "robotName")
            team.save()
            print("Updating info for team %s" % team_number)

    #########################################
    # Season Info
    #########################################
    @transaction.atomic
    def update_all_team_info(self, json_path):
        team_files_dir = json_path + "/teams"
        for _, _, files in os.walk(team_files_dir):
            for f in files:
                file_path = os.path.join(team_files_dir, f)
                self.__update_team_info(file_path)

    @transaction.atomic
    def update_competition_list(self, json_path):

        json_struct = self.__read_local_copy(json_path + "events/event_query.json")

        for event_info in json_struct["Events"]:
            code = event_info["code"]
            event = self.competition_model.objects.create(code=code)

            event.name = event_info["name"]
            event.city = event_info["city"]
            event.state = event_info["stateprov"]
            event.country = event_info["country"]
            event.save()

            print("Adding event %s" % code)

    #########################################
    # Competition Info
    #########################################

    @transaction.atomic
    def update_team_info(self, event_code, json_path):

        local_file = json_path + '/{0}_team_query.json'.format(event_code)
        if not os.path.exists(local_file):
            print("No team info, skipping population")
            return

        json_struct = self.__read_local_copy(local_file)

        for team_info in json_struct["teams"]:
            team_number = team_info["teamNumber"]

            team, _ = self.team_model.objects.get_or_create(teamNumber=team_number)
#             team.teamHomepage = team_info["website"] if team_info["website"] != None else "NA"
#             team.teamFirstYear = team_info["rookieYear"]
            team.homepage = self.__get_non_null_field(team_info, "website")
            team.rookie_year = self.__get_non_null_field(team_info, "rookieYear")
            team.city = self.__get_non_null_field(team_info, "city")
            team.state = self.__get_non_null_field(team_info, "stateProv")
            team.country = self.__get_non_null_field(team_info, "country")
            team.team_name = self.__get_non_null_field(team_info, "nameFull")
            team.team_nickname = self.__get_non_null_field(team_info, "nameShort")
            team.robot_name = self.__get_non_null_field(team_info, "robotName")
            team.save()
            print("Updating info for team %s" % team_number)

    @transaction.atomic
    def update_schedule(self, event_code, json_path):

        competition = self.competition_model.objects.get(code=event_code)

        local_file = json_path + '/{0}_schedule_query.json'.format(event_code)
        if not os.path.exists(local_file):
            print("No schedule info, skipping population")
            return

        json_struct = self.__read_local_copy(local_file)

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
            official_sr_search = self.official_match_sr_model.objects.filter(official_match=official_match)
            match_search = self.match_model.objects.filter(matchNumber=match_number)

            for team in red_teams + blue_teams:
                self.team_competes_in_model.objects.get_or_create(team=team, competition=competition)

            if len(match_search) == 0:
                match = self.match_model.objects.create(matchNumber=match_number, competition=competition, 
                                                        red1=red_teams[0], red2=red_teams[1], red3=red_teams[2], 
                                                        blue1=blue_teams[0], blue2=blue_teams[1], blue3=blue_teams[2])
            else:
                match = match_search[0]

                match.red1 = red_teams[0]
                match.red2 = red_teams[1]
                match.red3 = red_teams[2]
                match.blue1 = blue_teams[0]
                match.blue2 = blue_teams[1]
                match.blue3 = blue_teams[2]
                match.save()
                print("Updating teams for match %s" % match.matchNumber)

            if len(official_sr_search) == 0:
                self.official_match_sr_model.objects.create(official_match=official_match, competition=competition)
                self.official_match_sr_model.objects.create(official_match=official_match, competition=competition)
                print("Creating official match %s" % official_match.matchNumber)

    @transaction.atomic
    def update_matchresults(self, event_code, json_path):
        competition = self.competition_model.objects.get(code=event_code)

        local_file = json_path + '/{0}_scoreresult_query.json'.format(event_code)
        if not os.path.exists(local_file):
            print("No official results, skipping population")
            return

        json_struct = self.__read_local_copy(local_file)

        scores_info = json_struct["MatchScores"]
        for match_info in scores_info:
            match_number = match_info["matchNumber"]

            official_match = self.official_match_model.objects.get_or_create(matchNumber=match_number, competition=competition)[0]
            official_sr_search = self.official_match_sr_model.objects.filter(official_match=official_match)
            if len(official_sr_search) != 2:
                comp1 = self.official_match_sr_model.objects.create(competition=competition, official_match=official_match, alliance_color='R')
                comp2 = self.official_match_sr_model.objects.create(competition=competition, official_match=official_match, alliance_color='B')
                official_sr_search = [comp1, comp2]

            red_breakdown = [x for x in match_info["Alliances"] if x["alliance"] == "Red"][0]
            blue_breakdown = [x for x in match_info["Alliances"] if x["alliance"] == "Blue"][0]

            self._populate_official_sr(official_sr_search[0], red_breakdown, "R")
            self._populate_official_sr(official_sr_search[1], blue_breakdown, "B")

            print("Adding stats to official match %s" % official_match.matchNumber)
