'''
Created on Mar 2, 2017

@author: PJ
'''
from BaseScouting.api_scraper_TheBlueAlliance.ApiDownloader import ApiDownloader
import json
from BaseScouting.api_scraper_TheBlueAlliance.PopulateResultsFromApi import PopulateResultsFromApi
from BaseScouting.load_django import load_django
from Scouting2017.api_scraper_TheBlueAlliance.PopulateResultsFromApi2017 import PopulateResultsFromApi2017

load_django()

from Scouting2017.model.reusable_models import Team, Match, Competition, OfficialMatch
from Scouting2017.model.models2017 import OfficialMatchScoreResult

download_season_info = True
json_root = r'C:\Users\PJ\GitHub\SnobotScouting\scouting-app\ScoutingWebsite\Scouting2017\api_scraper_TheBlueAlliance\results'

# if download_season_info:
#     scraper = ApiDownloader(json_root)
#     scraper.download_matches_data("2017mndu2", 1)
# #     scraper.download_team_data()

populater = PopulateResultsFromApi2017()

event_codes = []
event_codes.append("2017flwp")
event_codes.append("2017milak")
event_codes.append("2017mndu")
event_codes.append("2017mndu2")
event_codes.append("2017mxtl")
event_codes.append("2017scmb")
event_codes.append("2017txlu")

for event_code in event_codes:
    with open(r'C:\Users\PJ\GitHub\SnobotScouting\scouting-app\ScoutingWebsite\Scouting2017\api_scraper_TheBlueAlliance\results\week1\%s_matches.json' % event_code) as f:
        json_results = json.load(f)
        populater.populate_schedule_match(json_results)

# event_json = """
# {
#   "message_data": {
#     "event_name": "New England FRC Region Championship",
#     "match": {
#       "comp_level": "q",
#       "match_number": 1,
#       "videos": [],
#       "time_string": "3:18 PM",
#       "set_number": 1,
#       "key": "2014necmp_f1m1",
#       "time": 1397330280,
#       "score_breakdown": null,
#       "alliances": {
#         "blue": {
#           "score": 154,
#           "teams": [
#             "frc177",
#             "frc230",
#             "frc4055"
#           ]
#         },
#         "red": {
#           "score": 78,
#           "teams": [
#             "frc195",
#             "frc558",
#             "frc5122"
#           ]
#         }
#       },
#       "event_key": "2014necmp"
#     }
#   },
#   "message_type": "match_score"
# }
# """
#
# json_data = json.loads(event_json)
#
# populater.populate_single_match(json_data["message_data"]["match"], json_data["message_data"]["match"]["event_key"])
# print json_data
