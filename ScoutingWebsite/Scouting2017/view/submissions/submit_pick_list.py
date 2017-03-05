'''
Created on Mar 4, 2017

@author: PJ
'''

from BaseScouting.views.submissions.submit_pick_list import BaseSubmitPickList
from Scouting2017.model.reusable_models import PickList, Competition, Team


class SubmitPickList2017(BaseSubmitPickList):

    def __init__(self):

        groupings = ["Overall", "Fuel", "Gear", "Defense", "Do Not Pick"]
        BaseSubmitPickList.__init__(groupings, Competition, PickList, Team)
