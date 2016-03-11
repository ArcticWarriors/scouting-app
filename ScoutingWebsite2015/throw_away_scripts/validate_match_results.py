'''
Created on Mar 9, 2016

@author: PJ
'''


from load_django import load_django
load_django()

from Scouting2016.models import Match, OfficialMatch, validate_match


def validate_matches():

    matches = Match.objects.all()
#     matches = Match.objects.filter(id=1)

    for match in matches:
        official_match = OfficialMatch.objects.get(matchNumber=match.matchNumber)

        if not official_match.hasOfficialData:
            continue

        valid, invalid_results = validate_match(match, official_match)
        if not valid:
            print "Match %s has errors: %s" % (match.matchNumber, invalid_results)

#         field_to_check = " Available Defenses"
#         if ("Blue" + field_to_check) in invalid_results or ("Red" + field_to_check) in invalid_results:
#             print "Match %s has errors: %s" % (match.matchNumber, invalid_results)

validate_matches()
