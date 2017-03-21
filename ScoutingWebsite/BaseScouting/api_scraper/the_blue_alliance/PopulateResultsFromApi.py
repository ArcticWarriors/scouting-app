'''
Created on Mar 2, 2017

@author: PJ
'''
import re
from django.db import transaction
import os
import json


class PopulateResultsFromApi:

    def __init__(self, team_model, team_competes_in_model, match_model, competition_model, official_match_model, official_match_sr_model):
        self.team_model = team_model
        self.team_competes_in_model = team_competes_in_model
        self.match_model = match_model
        self.competition_model = competition_model
        self.official_match_model = official_match_model
        self.official_match_sr_model = official_match_sr_model

    @transaction.atomic
    def populate_teams(self, json_path):
        team_files_dir = json_path + "/teams"
        for _, _, files in os.walk(team_files_dir):
            for f in files:
                file_path = os.path.join(team_files_dir, f)
                self.__update_team_info(file_path)

    @transaction.atomic
    def populate_events(self, json_path):
        json_struct = self.__read_local_copy(json_path + "/events.json")
        json_struct = [x for x in json_struct if x["week"] != None]
        json_struct = sorted(json_struct, key=lambda x: x["week"])

        for event_info in json_struct:
            code = event_info["event_code"].upper()
            event, _ = self.competition_model.objects.get_or_create(code=code)

            event.name = event_info["short_name"]
            event.location = event_info["location"]
            event.week = event_info['week'] + 1
            event.save()
#         print json_struct
#         team_files_dir = json_path + "/teams"
#         for _, _, files in os.walk(team_files_dir):
#             for f in files:
#                 file_path = os.path.join(team_files_dir, f)
#                 self.__update_team_info(file_path)

    @transaction.atomic
    def populate_competes_in(self, json_path, event_code):

        sanitized_event_code = re.findall("[0-9]*(.*)", event_code)[0]
        sanitized_event_code = sanitized_event_code.upper()

        json_struct = self.__read_local_copy(json_path)
        for team_json in json_struct:
            team_number = team_json['team_number']
            competition = self.competition_model.objects.get(code=sanitized_event_code)
            team = self.team_model.objects.get(teamNumber=team_number)
            self.team_competes_in_model.objects.get_or_create(team=team, competition=competition)

    @transaction.atomic
    def populate_schedule_match(self, match_json):

        if len(match_json) != 0:
            event_code = match_json[0]["event_key"]
            print "Updating schedule for... %s" % event_code

            for match in match_json:
                self.populate_single_match(match)
        else:
            print "No match data, ignoring"

    @transaction.atomic
    def populate_single_match(self, match_json):

        event_code = str(match_json["event_key"])
        sanitized_event_code = re.findall("[0-9]*(.*)", event_code)[0]
        sanitized_event_code = sanitized_event_code.upper()

        if match_json["comp_level"] != "qm":
            print "Not a quals match, ignoring"
        else:
            match_number = match_json["match_number"]

            competition, _ = self.competition_model.objects.get_or_create(code=sanitized_event_code)
            official_match, _ = self.official_match_model.objects.get_or_create(competition=competition, matchNumber=match_number)

            red_sr, _ = self.official_match_sr_model.objects.get_or_create(competition=competition, official_match=official_match, alliance_color="R")
            blue_sr, _ = self.official_match_sr_model.objects.get_or_create(competition=competition, official_match=official_match, alliance_color="B")

            alliances = match_json["alliances"]
            create_match_kwargs = self.__get_match_kwargs(competition, alliances)
            self.match_model.objects.get_or_create(competition=competition, matchNumber=match_number, **create_match_kwargs)

            if match_json["score_breakdown"]:
                self._populate_official_sr(red_sr, match_json["score_breakdown"]["red"], "R")
                self._populate_official_sr(blue_sr, match_json["score_breakdown"]["blue"], "B")

                if not official_match.hasOfficialData:
                    official_match.hasOfficialData = True
                    official_match.save()

    def _populate_official_sr(self, official_match_sr, alliance_info, alliance_color):
        raise NotImplementedError()

    def __update_team_info(self, local_file):

        if not os.path.exists(local_file):
            print("No team info, skipping population")
            return

        json_struct = self.__read_local_copy(local_file)

        for team_info in json_struct:
            team_number = team_info["team_number"]

            team, _ = self.team_model.objects.get_or_create(teamNumber=team_number)
            team.homepage = self.__get_non_null_field(team_info, "website")
            team.rookie_year = self.__get_non_null_field(team_info, "rookie_year")
            team.city = self.__get_non_null_field(team_info, "locality")
            team.state = self.__get_non_null_field(team_info, "region")
            team.country = self.__get_non_null_field(team_info, "country_name")
            team.team_name = self.__get_non_null_field(team_info, "name")
            team.team_nickname = self.__get_non_null_field(team_info, "nickname")
            # team.robot_name = self.__get_non_null_field(team_info, "robotName")
            team.save()

    def __get_match_kwargs(self, competition, alliance):
        output = {}

        for alliance_color in alliance.keys():
            teams = alliance[alliance_color]["teams"]
            for i, team_info in enumerate(teams):
                team_number = int(team_info[3:])
                team, _ = self.team_model.objects.get_or_create(teamNumber=team_number)
                self.team_competes_in_model.objects.get_or_create(team=team, competition=competition)
                output["%s%s" % (alliance_color, i + 1)] = team

        return output

    def __read_local_copy(self, input_file):
        with open(input_file, 'r') as f:
            response_body = f.read()

        json_struct = json.loads(response_body)

        return json_struct

    def __get_non_null_field(self, team_info, field_name, default="Unknown"):

        return team_info[field_name] if team_info[field_name] != None else default
