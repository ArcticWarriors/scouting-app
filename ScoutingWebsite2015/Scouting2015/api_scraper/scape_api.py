'''
Created on Feb 28, 2016

@author: PJ
'''
import os
import json
from urllib2 import Request, urlopen
#
from Scouting2015.api_scraper.api_key import get_encoded_key
import datetime


class ApiScraper():

    __api_website = "https://frc-api.firstinspires.org/v2.0/"

    def __init__(self, season, json_path):
        self.season = season
        self.json_path = json_path

    def get_header(self):

        headers = {}
        headers['Accept'] = 'application/json'
        headers['Authorization'] = 'Basic ' + get_encoded_key()

        return headers

    def read_url_and_dump(self, url, output_file):
        request = Request(url, headers=self.get_header())
        response_body = urlopen(request).read()

        json_struct = json.loads(response_body)

        dir_name = os.path.dirname(output_file)
        if not os.path.exists(dir_name):
            print "Creating directory at %s" % dir_name
            os.makedirs(dir_name)

        with open(output_file, 'w') as f:
            json.dump(json_struct, f, indent=4, separators=(',', ': '))

        return json_struct

    def download_team_data(self):
        url = self.__api_website + "/{0}/teams?".format(self.season)
        local_file = self.json_path + 'teams/team_query.json'
        json_struct = self.read_url_and_dump(url, local_file)

        total_pages = json_struct["pageTotal"]

        for page_i in range(total_pages):
            url = self.__api_website + "/{0}/teams?page={1}".format(self.season, page_i + 1)
            local_file = self.json_path + 'team_query_page%s.json' % page_i
            json_struct = self.read_url_and_dump(url, local_file)

    def download_event_data(self):
        url = self.__api_website + "/{0}/events?".format(self.season)
        local_file = self.json_path + 'events/event_query.json'
        self.read_url_and_dump(url, local_file)

        self.calculate_event_to_week_mapping()

    def calculate_event_to_week_mapping(self):
        local_file = self.json_path + 'events/event_query.json'

        with open(local_file, 'r') as f:
            event_list = json.loads(f.read())['Events']

        competitions = []
        min_week = 1000
        for event_json in event_list:
            code = event_json["code"]
            start_date = event_json["dateStart"]
            start_week = datetime.datetime.strptime(start_date, '%Y-%m-%dT00:00:00').isocalendar()[1]
            competitions.append((code, start_week))
            if start_week < min_week:
                min_week = start_week

        sorted_comp = []
        for x in sorted(competitions, key=lambda pair: pair[1]):
            sorted_comp.append((x[0], x[1] - min_week + 1))

        event_dump = self.json_path + 'events/event_week_mapping.json'
        with open(event_dump, 'w') as f:
            json.dump(sorted_comp, f, indent=4)

    def download_team_info(self, event_code):

        url = self.__api_website + "/{0}/teams?eventCode={1}".format(self.season, event_code)
        local_file = self.json_path + '/{0}_team_query.json'.format(event_code)
        self.read_url_and_dump(url, local_file)

    def download_schedule(self, event_code, tourny_level="Qualification"):
        url = self.__api_website + "/{0}/schedule/{1}?tournamentLevel={2}".format(self.season, event_code, tourny_level)
        local_file = self.json_path + '/{0}_schedule_query.json'.format(event_code)
        json_struct = self.read_url_and_dump(url, local_file)

        if len(json_struct["Schedule"]) == 0:
            print "Event %s does not have any schedule information" % event_code
            os.remove(local_file)

    def download_matchresult_info(self, event_code, start, ):
        raise

json_root = os.path.abspath("../__api_scraping_results") + "/"
if not os.path.exists(json_root):
    os.makedirs(json_root)

scraper = ApiScraper(2015, json_root)
# scraper.download_event_data()
scraper.download_team_data()


