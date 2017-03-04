'''
Created on Mar 2, 2017

@author: PJ
'''
from BaseScouting.api_scraper_TheBlueAlliance.ApiDownloader import ApiDownloader
import json
from BaseScouting.api_scraper_TheBlueAlliance.PopulateResultsFromApi import PopulateResultsFromApi
from BaseScouting.load_django import load_django
from Scouting2017.api_scraper_TheBlueAlliance.PopulateResultsFromApi2017 import PopulateResultsFromApi2017
import os
from Scouting2017.api_scraper_TheBlueAlliance.results.events_to_week import get_event_to_week_mapping

load_django()

download_events_info = False
download_matches = True
populate_results = False
year = 2017

json_root = os.path.abspath('results')

weeks_to_download = [0]  # off by one
event_codes = get_event_to_week_mapping()

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
