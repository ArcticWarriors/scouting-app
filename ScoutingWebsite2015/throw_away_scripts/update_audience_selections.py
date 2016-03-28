'''
Created on Feb 21, 2016

@author: PJ
'''
from load_django import load_django





def update_audience_selections(starting_category, matches_on):
    from Scouting2016.model import OfficialMatch

    category = starting_category
    official_matches = OfficialMatch.objects.all()
    match_ctr = 0
    
    for m in official_matches:

        print "Match %s, %s" % (m.matchNumber, category)
        m.audienceSelectionCategory = category
        m.save()
        
        match_ctr += 1
        
        if match_ctr == matches_on:
            category = chr(ord(category) + 1)
            match_ctr = 0
            
            if category == 'E':
                category = 'A'


load_django()
update_audience_selections('B', 8)

