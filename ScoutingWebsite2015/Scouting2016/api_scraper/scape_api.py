'''
Created on Feb 28, 2016

@author: PJ
'''
import os
import subprocess
import sys

# Hack for the command line
# os.chdir("..")
sys.path.append(os.path.abspath(".."))
print "\n".join(x for x in sys.path)

from Scouting2016.api_scraper.get_competitions import get_competitions_to_scrape


#############################################################
# Load django settings so this can be run as a one-off script
#############################################################
def reload_django(event_code, database_path):
    import os

    with open('../ScoutingWebsite/database_path.py', 'w') as f:
        f.write("database_path = '" + database_path + "/%s.sqlite3'" % event_code)

    cur_dir = os.getcwd()
    os.chdir("..")
    subprocess.call(["python", "manage.py", "migrate"])
    os.chdir(cur_dir)

#############################################################

import json
from urllib2 import Request, urlopen

from Scouting2016.api_scraper.api_key import get_encoded_key


__api_website = "https://frc-api.firstinspires.org/v2.0/"


def get_header():

    headers = {}
    headers['Accept'] = 'application/json'
    headers['Authorization'] = 'Basic ' + get_encoded_key()

    return headers


def read_url_and_dump(url, headers, output_file):
    request = Request(url, headers=headers)
    response_body = urlopen(request).read()

    json_struct = json.loads(response_body)

    with open(output_file, 'w') as f:
        json.dump(json_struct, f, indent=4, separators=(',', ': '))

    return json_struct


def download_team_data(json_path, season="2016"):
    url = __api_website + "/{0}/teams?".format(season)
    local_file = json_path + 'teams/team_query.json'
    json_struct = read_url_and_dump(url, get_header(), local_file)

    total_pages = json_struct["pageTotal"]

    for page_i in range(total_pages):
        url = __api_website + "/{0}/teams?page={1}".format(season, page_i + 1)
        local_file = json_path + 'team_query_page%s.json' % page_i
        json_struct = read_url_and_dump(url, get_header(), local_file)


def download_event_data(json_path, season="2016"):
    url = __api_website + "/{0}/events?".format(season)
    local_file = json_path + 'events/event_query.json'
    json_struct = read_url_and_dump(url, get_header(), local_file)


def download_team_info(event_code, json_path, season="2016"):

    url = __api_website + "/{0}/teams?eventCode={1}".format(season, event_code)
    local_file = json_path + '/{0}_team_query.json'.format(event_code)
    read_url_and_dump(url, get_header(), local_file)


def download_matchresult_info(event_code, start, json_path, season="2016", tourny_level="Qualification"):
    url = __api_website + "/{0}/scores/{1}/{2}?start={3}".format(season, event_code, tourny_level, start)
    local_file = json_path + '/{0}_scoreresult_query.json'.format(event_code)
    json_struct = read_url_and_dump(url, get_header(), local_file)

    if len(json_struct["MatchScores"]) == 0:
        print "Event %s does not have any match results" % event_code
        os.remove(local_file)


def download_schedule(event_code, start, json_path, season="2016", tourny_level="Qualification"):
    url = __api_website + "/{0}/schedule/{1}?tournamentLevel={2}&start={3}".format(season, event_code, tourny_level, start)
    local_file = json_path + '/{0}_schedule_query.json'.format(event_code)
    json_struct = read_url_and_dump(url, get_header(), local_file)

    if len(json_struct["Schedule"]) == 0:
        print "Event %s does not have any schedule information" % event_code
        os.remove(local_file)

match_start = 0
download_results = True
update_database = True

if download_results:
    json_path = "../__api_scraping_results/json/"
#     download_team_data(json_path)
    download_event_data(json_path)

# for json_path, sql_path, ec in get_competitions_to_scrape():
#
#     if download_results:
#         print "Downloading results for regional %s" % ec
#         download_matchresult_info(ec, match_start, json_path)
#         download_schedule(ec, match_start, json_path)
#         download_team_info(ec, json_path)
#
#     if update_database:
#         reload_django(ec, sql_path)
#         subprocess.call(['python', 'populate_database.py', ec, sql_path, json_path])
#         pass
