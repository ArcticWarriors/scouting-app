from django.views.generic.base import View
from django.http.response import HttpResponse
import re
import json


class BaseSubmitMatchEdit(View):

    def __init__(self, competition_model, match_model, team_model, score_result_model, official_match_model):

        self.competition_model = competition_model
        self.match_model = match_model
        self.team_model = team_model
        self.score_result_model = score_result_model
        self.official_match_model = official_match_model

    def post(self, request, **kargs):

        success = False

        creation_dict = {}

        try:
            for arg in request.POST:
                matches = re.findall("edit_([0-9]+)_(.*)", arg)
                if len(matches) == 1:
                    team_number, field = matches[0]
                    if team_number not in creation_dict:
                        creation_dict[team_number] = {}

                    creation_dict[team_number][field] = request.POST[arg]
    #                 print team_number, field

            competition = self.competition_model.objects.get(code=kargs['regional_code'])
            match = self.match_model.objects.get(competition=competition, matchNumber=request.POST['match_number'])
            for team_number in creation_dict:
                team = self.team_model.objects.get(teamNumber=team_number)
                sr = self.score_result_model.objects.get(competition=competition, team=team, match=match)

                for key, value in creation_dict[team_number].iteritems():
                    attr = getattr(sr, key)
                    if type(attr) is bool:
                        value = self.__convertBool(value)
                        setattr(sr, key, value)
                    else:
                        setattr(sr, key, value)

                sr.save()
            success = True

        except Exception as e:
            print "ERROR %s" % e

        output = {}
        print "Got here"
        if success:
            try:
                official_match_search = self.official_match_model.objects.filter(competition=competition, matchNumber=match.matchNumber)
                if len(official_match_search) == 1:
                    official_match = official_match_search[0]
                    official_sr_search = official_match.officialmatchscoreresult_set.all()
                    if len(official_sr_search) == 2:
                        _, warning_messages, error_messages = self._recalculate_official_results_validity(match, official_match, official_sr_search)

                        official_results = {}
                        official_results["warning_messages"] = warning_messages
                        official_results["error_messages"] = error_messages
                        output["official_match_validation"] = official_results
            except Exception as e:
                print "Error %s" % e
                success = False

        output["success"] = success
        print output

        return HttpResponse(json.dumps(output), content_type='application/json')

    def _recalculate_official_results_validity(self, match, official_match, official_sr_search):
        raise NotImplementedError("You need to implement the _recalculate_official_results_validity function!")

    def __convertBool(self, value):

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
