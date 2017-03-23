'''
Created on Mar 21, 2017

@author: PJ
'''
from django.http.response import HttpResponse
import csv
from Scouting2017.model.reusable_models import Match, OfficialMatch
import operator
from Scouting2017.model.validate_match import calculate_match_scouting_validity


def download_match_inconsistancies(request, regional_code):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="match_inconsistancies.csv"'

    file_output = "Match Number\tRed Teams Missing\tBlue Teams Missing\tDuplicate Teams\tExtra Teams\tWarnings\tErrors\n"

    matches = Match.objects.filter(competition__code=regional_code)
    matches = sorted(matches, key=operator.attrgetter('matchNumber'))

    for match in matches:

        if match.scoreresult_set.count() == 0:
            continue

        official_match_search = OfficialMatch.objects.filter(competition__code=regional_code, matchNumber=match.matchNumber)
        if len(official_match_search) == 1:
            official_match = official_match_search[0]
            official_sr_search = official_match.officialmatchscoreresult_set.all()
            if len(official_sr_search) == 2:
                _, red_missing, blue_missing, duplicate_teams, extra_teams, warning_messages, error_messages = calculate_match_scouting_validity(match, official_match, official_sr_search)

                file_output += "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (match.matchNumber, red_missing, blue_missing, duplicate_teams, extra_teams, warning_messages, error_messages)

    response.write(file_output)

    return response
