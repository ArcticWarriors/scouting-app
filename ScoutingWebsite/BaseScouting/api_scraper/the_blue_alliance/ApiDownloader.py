'''
Created on Feb 28, 2016

@author: PJ
'''
import os
import json
import requests
from BaseScouting.api_scraper.the_blue_alliance.api_key import get_encoded_key


class ApiDownloader():

    __api_website = "https://www.thebluealliance.com/api/v2/"

    def __init__(self, json_path):
        self.json_path = json_path

    def __get_header(self):

        headers = {}
#         headers['Accept'] = 'application/json'
        headers['X-TBA-App-Id'] = get_encoded_key()

        return headers

    def read_url_and_dump(self, url, output_file):
        print url
        json_struct = requests.get(url, headers=self.__get_header()).json()

        dir_name = os.path.dirname(output_file)
        if not os.path.exists(dir_name):
            print("Creating directory at %s" % dir_name)
            os.makedirs(dir_name)

        with open(output_file, 'w') as f:
            json.dump(json_struct, f, indent=4, separators=(',', ': '))

        return json_struct

    def download_team_data(self):

        page_num = 0
        while True:
            url = self.__api_website + "teams/{0}".format(page_num)
            local_file = self.json_path + '/teams/team_query_page{0:02d}.json'.format(page_num)
            json_struct = self.read_url_and_dump(url, local_file)
            if len(json_struct) == 0:
                break

            page_num += 1

    def download_matches_data(self, event_code):
        url = self.__api_website + "event/%s/matches" % event_code
        local_file = self.json_path + '/%s_matches.json' % (event_code)
        print "Dumping matches from %s to %s" % (url, local_file)
        return self.read_url_and_dump(url, local_file)

    def download_event_data(self, year):
        url = self.__api_website + "events/%s" % year
        local_file = self.json_path + '/events.json'
        json_data = self.read_url_and_dump(url, local_file)
        self.__dump_week_to_event_mappings(json_data)

        return json_data



    def download_competes_in_data(self, year, event):
        url = self.__api_website + "event/%s%s/teams" % (year, event)
        local_file = self.json_path + '/%s_teams.json' % (event)

        return self.read_url_and_dump(url, local_file)



    def __dump_week_to_event_mappings(self, json_data):

        with open(self.json_path + "/events_to_week.py", 'w') as f:
            header = """
import collections


def get_event_to_week_mapping():
    output = collections.defaultdict(list)

"""

            f.write(header)

            mappings = []
            for event_json in json_data:
                week = event_json["week"]
                key = event_json["key"]

                if week != None:
                    print week
                    mappings.append((week + 1, key))

            mappings = sorted(mappings, key=lambda x: x[0])
            for mapping in mappings:
                f.write("    output[%s].append('%s')\n" % (mapping[0], mapping[1]))

            f.write("\n    return output\n")
# 
#     def calculate_event_to_week_mapping(self, first_week):
#         local_file = self.json_path + 'events/event_query.json'
# 
#         with open(local_file, 'r') as f:
#             event_list = json.loads(f.read())['Events']
# 
#         competitions = []
#         min_week = 1000
#         for event_json in event_list:
#             code = event_json["code"]
#             start_date = event_json["dateStart"]
#             start_week = datetime.datetime.strptime(start_date, '%Y-%m-%dT00:00:00').isocalendar()[1]
#             competitions.append((code, start_week))
#             if start_week < min_week:
#                 min_week = start_week
# 
#         if first_week != None:
#             min_week = first_week
#             print "Overriding first week..."
# 
#         sorted_comp = []
#         for x in sorted(competitions, key=lambda pair: pair[1]):
#             sorted_comp.append((x[0], x[1] - min_week + 1))
# 
#         event_dump = self.json_path + 'events/event_week_mapping.json'
#         with open(event_dump, 'w') as f:
#             json.dump(sorted_comp, f, indent=4)
# 
# 
#     def download_matchresult_info(self, event_code, competition_week, tourny_level="Qualification"):
#         url = self.__api_website + "/{0}/scores/{1}/{2}".format(self.season, event_code, tourny_level)
#         local_file = self.json_path + '/week{0}/{1}_scoreresult_query.json'.format(competition_week, event_code)
#         try:
#             json_struct = self.read_url_and_dump(url, local_file)
# 
#             if len(json_struct["MatchScores"]) == 0:
#                 print("Event %s does not have any match results" % event_code)
#                 os.remove(local_file)
#         except urllib2.HTTPError:
#             print("Event %s has invalid match results" % event_code)
