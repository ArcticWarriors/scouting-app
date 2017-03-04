'''
Created on Mar 2, 2017

@author: PJ
'''
from BaseScouting.api_scraper_TheBlueAlliance.ApiDownloader import ApiDownloader
from BaseScouting.load_django import load_django
from Scouting2017.api_scraper_TheBlueAlliance.PopulateResultsFromApi2017 import PopulateResultsFromApi2017
from Scouting2017.api_scraper_TheBlueAlliance.results.events_to_week import get_event_to_week_mapping
import json
import os
import sys
import collections

load_django()

download_events_info = False
download_matches = True
populate_results = False
year = 2017

json_root = os.path.abspath('results')

event_codes = get_event_to_week_mapping()

# #################
# # Trim by weeks #
# #################
# weeks_to_download = [1]
# event_codes = {week: event_codes[week] for week in event_codes if week in weeks_to_download}

# #################
# # Trim by event #
# #################
# events_to_download = ["2017flwp", "2017milak", "2017misou", "2017mndu", "2017mndu2", "2017mxtl", "2017scmb", "2017txlu", "2017waspo"]
# trimmed_events = collections.defaultdict(list)
# for week, event_list in event_codes.items():
#     for code in event_list:
#         if code in events_to_download:
#             trimmed_events[week].append(code)
# event_codes = trimmed_events


if download_events_info:
    scraper = ApiDownloader(json_root)
    scraper.download_event_data(year)


if download_matches:
    for week, events_list in event_codes.items():
        for event_code in events_list:
            scraper = ApiDownloader(os.path.join(json_root, "week%s" % week))
            scraper.download_matches_data(event_code)


if populate_results:
    populater = PopulateResultsFromApi2017()

    for week, events_list in event_codes.items():
        for event_code in events_list:
            with open(os.path.join(json_root, r'week%s\%s_matches.json' % (week, event_code))) as f:
                json_results = json.load(f)
                populater.populate_schedule_match(json_results)
