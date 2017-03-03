'''
Created on Feb 25, 2017

@author: PJ
'''
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from BaseScouting.api_scraper_TheBlueAlliance.ApiDownloader import ApiDownloader
import datetime
import json


week_number = 1
json_root = r'C:\Users\PJ\GitHub\SnobotScouting\scouting-app\ScoutingWebsite\Scouting2017\api_scraper_TheBlueAlliance\results'


def __download_schedule(event_code):
    scraper = ApiDownloader(json_root)
    scraper.download_matches_data(event_code, week_number)


def __parse_schedule_updated(json_request):
    print "Parsing schedule"

    try:
        event_code = json_request["message_data"]["event_key"]
        __download_schedule(event_code)
    except Exception as e:
        print "ERROR: %s" % e


def __parse_match_score(json_request):
    print "Got match score"


@csrf_exempt
def tba_webook(request, **kargs):

    json_request = json.loads(request.body)
    message_type = str(json_request['message_type'])

    try:
        with open(r'C:\Users\PJ\GitHub\SnobotScouting\scouting-app\ScoutingWebsite\Scouting2017\api_scraper_TheBlueAlliance\tba_log.txt', 'a') as f:
            cur_time = datetime.datetime.now().time()
            f.write(str(cur_time) + " - " + request.body + "\n")
    except Exception as e:
        print e
        print "UH OH"

    if message_type == "schedule_updated":
        __parse_schedule_updated(json_request)
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
