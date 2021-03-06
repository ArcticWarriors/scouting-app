'''
Created on Apr 20, 2016

@author: PJ
'''
import os
import json
from BaseScouting.load_django import load_django
from BaseScouting.api_scraper_FIRST.ApiDownloader import ApiDownloader
from Scouting2016.api_scraper_FIRST.PopulateResultsFromApi2016 import PopulateRegionalresults2016

download_season_info = False
download_results = False
populate_results = True

year = 2016
json_root = os.path.abspath("../../Scouting{0}/__api_scraping_results".format(year)) + "/"

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

    if week == 9:
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
        print(event_path)
        populater = PopulateRegionalresults2016()
        populater.update_schedule(code, event_path)
        populater.update_matchresults(code, event_path)
