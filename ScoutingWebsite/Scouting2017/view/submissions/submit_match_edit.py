'''
Created on Mar 1, 2017

@author: PJ
'''
from Scouting2017.model.reusable_models import OfficialMatch, Competition, Match,\
    Team
from Scouting2017.model.validate_match import calculate_match_scouting_validity
import json
from django.http.response import HttpResponse
from Scouting2017.model.models2017 import ScoreResult
import re


def submit_match_edit(request, **kwargs):

    def convertBool(value):

        output = True

        if value.lower() == "true":
            output = True
        elif value.lower() == "false":
            output = False
        elif value.lower() == "yes":
            output = True
        elif value.lower() == "no":
            output = False
        elif value.lower() == "y":
            output = True
        elif value.lower() == "n":
            output = False
        elif value.lower() == "t":
            output = True
        elif value.lower() == "f":
            output = False

        return output

    success = False

    creation_dict = {}

    print kwargs

    try:
        for arg in request.POST:
            matches = re.findall("edit_([0-9]+)_(.*)", arg)
            if len(matches) == 1:
                team_number, field = matches[0]
                if team_number not in creation_dict:
                    creation_dict[team_number] = {}

                creation_dict[team_number][field] = request.POST[arg]
#                 print team_number, field

        competition = Competition.objects.get(code=kwargs['regional_code'])
        match = Match.objects.get(competition=competition, matchNumber=request.POST['match_number'])
        for team_number in creation_dict:
            team = Team.objects.get(teamNumber=team_number)
            sr = ScoreResult.objects.get(competition=competition, team=team, match=match)

            for key, value in creation_dict[team_number].iteritems():
                attr = getattr(sr, key)
                if type(attr) is bool:
                    value = convertBool(value)
                    setattr(sr, key, value)
                else:
                    setattr(sr, key, value)

            sr.save()
        success = True

    except Exception as e:
        print "ERROR %s" % e

    output = {}
    output["success"] = success
    if success:
        try:
            official_match_search = OfficialMatch.objects.filter(competition=competition, matchNumber=match.matchNumber)
            if len(official_match_search) == 1:
                official_match = official_match_search[0]
                official_sr_search = official_match.officialmatchscoreresult_set.all()
                if len(official_sr_search) == 2:
                    _, warning_messages, error_messages = calculate_match_scouting_validity(match, official_match, official_sr_search)

                    official_results = {}
                    official_results["warning_messages"] = warning_messages
                    official_results["error_messages"] = error_messages
                    output["official_match_validation"] = official_results
        except Exception as e:
            print "Error %s" % e
    print output

    return HttpResponse(json.dumps(output), content_type='application/json')
