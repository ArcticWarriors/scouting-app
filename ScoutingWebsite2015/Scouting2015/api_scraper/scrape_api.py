'''
Created on Apr 20, 2016

@author: PJ
'''
import os
import json
from api_scraper.ApiDownloader import ApiDownloader
from BaseScouting import load_django.load_django
from Scouting2015.api_scraper.PopulateResultsFromApi2015 import PopulateRegionalResults2015


year = 2015
json_root = os.path.abspath("../../Scouting{0}/__api_scraping_results".format(year)) + "/"

# scraper.download_event_data()
# scraper.download_team_data()

events_file = json_root + 'events/event_week_mapping.json'

with open(json_root + 'events/event_week_mapping.json', 'r') as f:
    json_struct = json.loads(f.read())

events_to_do = []
download_results = False
populate_results = True

for pair in json_struct:
    code = pair[0]
    week = pair[1]

    events_to_do.append((code, week))

# events_to_do.append(("NYRO", 4))

# populater = PopulateRegionalResults2015()

if download_results:
    pass

if populate_results:
    load_django()
    populater = PopulateRegionalResults2015()
#     populater.update_competition_list(json_root)
#     populater.update_all_team_info(json_root)

for event_pair in events_to_do:
    code = event_pair[0]
    week = event_pair[1]

    if download_results:
        scraper = ApiDownloader(year, json_root)
        scraper.download_schedule(code, week)
        scraper.download_matchresult_info(code, week)

    if populate_results:
        event_path = json_root + "week%s" % week
#         populater.update_schedule(code, event_path)
        populater.update_matchresults(code, event_path)

#     break
