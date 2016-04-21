'''
Created on Apr 20, 2016

@author: PJ
'''
# from .ApiDownloader import ApiDownloader
import os
import json
from ApiDownloader import ApiDownloader


year = 2016
json_root = os.path.abspath("../Scouting{0}/__api_scraping_results".format(year)) + "/"
scraper = ApiDownloader(year, json_root)

# scraper.download_event_data()
# scraper.download_team_data()

events_file = json_root + 'events/event_week_mapping.json'

with open(json_root + 'events/event_week_mapping.json', 'r') as f:
    json_struct = json.loads(f.read())

for pair in json_struct:
    scraper.download_schedule(pair[0], pair[1])
    scraper.download_matchresult_info(pair[0], pair[1])

