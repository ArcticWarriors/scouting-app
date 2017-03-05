'''
Created on Feb 25, 2017

@author: PJ
'''
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from BaseScouting.api_scraper.the_blue_alliance.ApiDownloader import ApiDownloader
from Scouting2017.api_scraper.the_blue_alliance.PopulateResultsFromApi2017 import PopulateResultsFromApi2017
import datetime
import json
import os


def __download_schedule(event_code, json_dump_dir):
    print "Download schedule", event_code, json_dump_dir
    scraper = ApiDownloader(json_dump_dir)
    json_data = scraper.download_matches_data(event_code)

    populater = PopulateResultsFromApi2017()
    populater.populate_schedule_match(json_data)


def __parse_schedule_updated(json_request, json_dump_dir):
    print "Parsing schedule"

    try:
        event_code = json_request["message_data"]["event_key"]
        __download_schedule(event_code, json_dump_dir)
    except Exception as e:
        print "ERROR: %s" % e
        raise


def __parse_match_score(json_request):

    print "Got match score"

    try:
        match_data = json_request["message_data"]["match"]

        populater = PopulateResultsFromApi2017()
        populater.populate_single_match(match_data)
    except Exception as e:
        print "ERROR: %s" % e
        raise


@csrf_exempt
def tba_webook(request, **kargs):

    json_request = json.loads(request.body)
    message_type = str(json_request['message_type'])

    week = 1

    dump_root = os.path.join(os.getcwd(), 'Scouting2017/api_scraper_TheBlueAlliance')
    json_dump_dir = os.path.join(os.getcwd(), 'Scouting2017/api_scraper_TheBlueAlliance/results/week%s' % week)
    try:
        dump_file = os.path.join(dump_root, 'tba_log.txt')
        print dump_file
        with open(dump_file, 'a') as f:
            cur_time = datetime.datetime.now().time()
            f.write(str(cur_time) + " - " + request.body + "\n")
    except Exception as e:
        print e
        print "UH OH"

    if message_type == "schedule_updated":
        __parse_schedule_updated(json_request, json_dump_dir)
    elif message_type == "match_score":
        __parse_match_score(json_request)
    elif message_type == "upcoming_match":
        print "Got upcoming match"
    elif message_type == "starting_comp_level":
        print "Comp Level"
    elif message_type == "alliance_selection":
        print "Alliance Selection"
    elif message_type == "ping":
        print "Got Ping message"
    else:
        print "UNKNOWN MESSAGE %s" % message_type

    html = "<html><body>Hello</body></html>"
    return HttpResponse(html)
