'''
Created on Mar 31, 2016

@author: PJ
'''

import os
import sys
import json
from django.core.wsgi import get_wsgi_application


def read_local_copy(input_file):
    with open(input_file, 'r') as f:
        response_body = f.read()

    json_struct = json.loads(response_body)

    return json_struct


def get_non_null_field(team_info, field_name, default="Unknown"):

    return team_info[field_name] if team_info[field_name] != None else default


def update_all_team_info(json_path):
    team_files_dir = json_path + "/teams"
    for _, _, files in os.walk(team_files_dir):
        for f in files:
            file_path = os.path.join(team_files_dir, f)
            update_team_info(file_path)


def update_team_info(local_file):
    from Scouting2016.model import Team

    if not os.path.exists(local_file):
        print("No team info, skipping population")
        return

    json_struct = read_local_copy(local_file)

    for team_info in json_struct["teams"]:
        team_number = team_info["teamNumber"]

        team, _ = Team.objects.get_or_create(teamNumber=team_number)
        team.homepage = get_non_null_field(team_info, "website")
        team.rookie_year = get_non_null_field(team_info, "rookieYear")
        team.city = get_non_null_field(team_info, "city")
        team.state = get_non_null_field(team_info, "stateProv")
        team.country = get_non_null_field(team_info, "country")
        team.team_name = get_non_null_field(team_info, "nameFull")
        team.team_nickname = get_non_null_field(team_info, "nameShort")
        team.robot_name = get_non_null_field(team_info, "robotName")
        team.save()
        print("Updating info for team %s" % team_number)


def update_event_info(json_path):
    from Scouting2016.model.reusable_models import Compitition

    json_struct = read_local_copy(json_path + "events/event_query.json")

    for event_info in json_struct["Events"]:
        code = event_info["code"]
        event = Compitition.objects.create(code=code)

        event.name = event_info["name"]
        event.city = event_info["city"]
        event.state = event_info["stateprov"]
        event.country = event_info["country"]
        print(event_info)
        event.save()

os.environ["DJANGO_SETTINGS_MODULE"] = "ScoutingWebsite.settings"
proj_path = os.path.abspath("..")
sys.path.append(proj_path)
_ = get_wsgi_application()

json_path = "../__api_scraping_results/json/"
# update_all_team_info(json_path)
update_event_info(json_path)
