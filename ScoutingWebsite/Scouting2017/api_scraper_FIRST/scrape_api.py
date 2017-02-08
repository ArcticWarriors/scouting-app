'''
Created on Apr 20, 2016

@author: PJ
'''
import os
import json
import sys

sys.path.append("../..")

from BaseScouting.load_django import load_django
from BaseScouting.api_scraper_FIRST.ApiDownloader import ApiDownloader
from Scouting2017.api_scraper_FIRST.PopulateResultsFromApi2017 import PopulateRegionalresults2017

download_season_info = True
download_results = True
populate_results = False

year = 2017
json_root = os.path.abspath("../../Scouting{0}/api_scraper_FIRST/api_scraping_results".format(year)) + "/"

if download_season_info:
    scraper = ApiDownloader(year, json_root)
    scraper.download_event_data(first_week=9)
    scraper.download_team_data()

events_file = json_root + 'events/event_week_mapping.json'
with open(events_file, 'r') as f:
    json_struct = json.loads(f.read())

events_to_do = []

for pair in json_struct:
    code = pair[0]
    week = pair[1]

    events_to_do.append((code, week))

if populate_results:
    load_django()


for event_pair in events_to_do:
    code = event_pair[0]
    week = event_pair[1]

    if download_results:
        scraper = ApiDownloader(year, json_root)
        scraper.download_schedule(code, week)
        scraper.download_matchresult_info(code, week)

    if populate_results:
        event_path = json_root + "week%s" % week
        print event_path

        populater = PopulateRegionalresults2017()
        populater.update_team_info(code, event_path)
        populater.update_schedule(code, event_path)
        populater.update_matchresults(code, event_path)
