'''
Created on Feb 21, 2016

@author: PJ
'''
from Scouting2016.models import OfficialMatch


def update_audience_selections(starting_category):

    category = starting_category
    official_matches = OfficialMatch.objects.all()
    for m in official_matches:

        m.audienceSelectionCategory = category
        m.save()

        category = chr(ord(category) + 1)
        if category == 'E':
            category = 'A'
