'''
Created on Mar 2, 2017

@author: PJ
'''
import re


class PopulateResultsFromApi:

    def __init__(self, team_model, match_model, competition_model, official_match_model, official_match_sr_model):
        self.team_model = team_model
        self.match_model = match_model
        self.competition_model = competition_model
        self.official_match_model = official_match_model
        self.official_match_sr_model = official_match_sr_model

    def populate_schedule_match(self, match_json):

        event_code = "UNKNOWN"
        if len(match_json) != 0:
            event_code = match_json[0]["event_key"]

        print "Updating schedule for... %s" % event_code

        for match in match_json:
            self.populate_single_match(match)

    def populate_single_match(self, match_json):

        event_code = str(match_json["event_key"])
        sanitized_event_code = re.findall("[0-9]*(.*)", event_code)[0]
        sanitized_event_code = sanitized_event_code.upper()

        if match_json["comp_level"] != "qm":
            print "Not a quals match, ignoring"
        else:
            match_number = match_json["match_number"]

            competition, _ = self.competition_model.objects.get_or_create(code=sanitized_event_code)
            official_match, _ = self.official_match_model.objects.get_or_create(competition=competition, matchNumber=match_number)

            red_sr, _ = self.official_match_sr_model.objects.get_or_create(competition=competition, official_match=official_match, alliance_color="R")
            blue_sr, _ = self.official_match_sr_model.objects.get_or_create(competition=competition, official_match=official_match, alliance_color="B")

            if match_json["score_breakdown"]:
                self.parse_score_breakdown(match_json["score_breakdown"], red_sr, blue_sr)

    def parse_score_breakdown(self, score_breakdown, red_official_sr, blue_official_sr):
        print "Override me!"
