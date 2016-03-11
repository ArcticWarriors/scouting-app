'''
Created on Feb 28, 2016

@author: PJ
'''
import subprocess
from api_scraper import get_users


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

from api_scraper.api_key import get_encoded_key


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


def download_team_info(event_code, json_path, season="2016"):

    url = __api_website + "/{0}/teams?eventCode={1}".format(season, event_code)
    local_file = json_path + '/{0}_team_query.json'.format(event_code)
    read_url_and_dump(url, get_header(), local_file)


def download_matchresult_info(event_code, start, json_path, season="2016", tourny_level="Qualification"):
    url = __api_website + "/{0}/scores/{1}/{2}?start={3}".format(season, event_code, tourny_level, start)
    local_file = json_path + '/{0}_scoreresult_query.json'.format(event_code)
    read_url_and_dump(url, get_header(), local_file)


def download_schedule(event_code, start, json_path, season="2016", tourny_level="Qualification"):
    url = __api_website + "/{0}/schedule/{1}?tournamentLevel={2}&start={3}".format(season, event_code, tourny_level, start)
    local_file = json_path + '/{0}_schedule_query.json'.format(event_code)
    read_url_and_dump(url, get_header(), local_file)


# Week 1
event_codes = []
# event_codes.append("ONTO2")
# event_codes.append("ISTA")
# event_codes.append("MNDU")
# event_codes.append("MNDU2")
# event_codes.append("SCMB")
# event_codes.append("CASD")
# event_codes.append("VAHAY")
# event_codes.append("MIKET")
# event_codes.append("MISOU")
# event_codes.append("MISTA")
# event_codes.append("MIWAT")
# event_codes.append("PAHAT")
# event_codes.append("NJFLA")
# event_codes.append("NCMCL")
# event_codes.append("NHGRS")
event_codes.append("CTWAT")
# event_codes.append("WAAMV")
# event_codes.append("WASPO")

match_start = 0
download_results = False
update_database = True
json_path = "../__api_scraping_results/json/week1"
sql_path = "__api_scraping_results/database/week1"

for ec in event_codes:

    if download_results:
        print "Downloading results for regional %s" % ec
        download_matchresult_info(ec, match_start, json_path)
        download_schedule(ec, match_start, json_path)
        download_team_info(ec, json_path)

    if update_database:
        reload_django(ec, sql_path)
        subprocess.call(['python', 'populate_database.py', ec, sql_path, json_path])
        pass

#     reload_django(ec, sql_path)
#     add_users()
