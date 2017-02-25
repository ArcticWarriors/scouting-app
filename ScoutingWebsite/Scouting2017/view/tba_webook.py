'''
Created on Feb 25, 2017

@author: PJ
'''
from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


def __parse_schedule_updated(json_request):
    print "Parsing schedule"


def __parse_match_score(json_request):
    print "Got match score"


@csrf_exempt
def tba_webook(request, **kargs):
    
    json_request = json.loads(request.body)
    message_type = str(json_request['message_type'])
    
    try:
        with open(r'C:\Users\PJ\GitHub\SnobotScouting\scouting-app\ScoutingWebsite\Scouting2017\api_scraper_TheBlueAlliance\tba_log.txt', 'a') as f:
            f.write(request.body + "\n")
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
    else:
        print "UNKNOWN MESSAGE %s" % message_type
     
    html = "<html><body>Hello</body></html>"
    return HttpResponse(html)
