'''
Created on Feb 22, 2017

@author: PJ
'''
from BaseScouting.views.base_views import BaseMatchEntryView


class MatchEntryView2017(BaseMatchEntryView):
    def __init__(self):
        BaseMatchEntryView.__init__(self, 'Scouting2017/match_entry.html')
