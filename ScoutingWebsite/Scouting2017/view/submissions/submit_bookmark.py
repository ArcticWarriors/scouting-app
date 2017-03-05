'''
Created on Mar 1, 2017

@author: PJ
'''
from Scouting2017.model.reusable_models import Team
from BaseScouting.views.submissions.submit_bookmark import BaseUpdateBookmarks


class UpdateBookmarks2017(BaseUpdateBookmarks):

    def __init__(self):
        BaseUpdateBookmarks.__init__(self, Team)
