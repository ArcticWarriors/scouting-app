'''
Created on Mar 5, 2017

@author: PJ
'''
from BaseScouting.api_scraper.fake_data_scripts.random_helpers import getBoolWithPercentage
import math


class Robot:

    def __init__(self,
                 auto_mobility_percentage=95,
                 auto_gear_percentage=40,
                 auto_high_goal_percentage=0,
                 auto_high_goal_capacity=10,
                 auto_low_goal_percentage=0,
                 auto_low_goal_capacity=10,

                 climb_percentage=50,
                 tele_low_goal_percentage=0,
                 tele_low_goal_capacity=0,
                 tele_high_goal_percentage=0,
                 tele_high_goal_capacity=0,
                 tele_gear_max=2,
                 tele_gear_consistancy=50,

                 foul_percentage=5,
                 tech_foul_percentage=1):

        self.auto_auto_mobility_percentage = auto_mobility_percentage
        self.auto_gear_percentage = auto_gear_percentage
        self.auto_high_goal_percentage = auto_high_goal_percentage
        self.auto_high_goal_capacity = auto_high_goal_capacity
        self.auto_low_goal_percentage = auto_low_goal_percentage
        self.auto_low_goal_capacity = auto_low_goal_capacity

        self.climb_percentage = climb_percentage
        self.tele_low_goal_percentage = tele_low_goal_percentage
        self.tele_low_goal_capacity = tele_low_goal_capacity
        self.tele_high_goal_percentage = tele_high_goal_percentage
        self.tele_high_goal_capacity = tele_high_goal_capacity
        self.tele_gear_max = tele_gear_max
        self.tele_gear_consistancy = tele_gear_consistancy

        self.foul_percentage = foul_percentage
        self.tech_foul_percentage = tech_foul_percentage

    def create_score_result(self):

        output = {}
        output['auto_mobility'] = 'Mobility' if getBoolWithPercentage(self.auto_auto_mobility_percentage) else 'None'
        output['auto_gear'] = 1 if getBoolWithPercentage(self.auto_gear_percentage) else 0
        output['auto_fuel_high'] = math.floor(self.auto_high_goal_percentage * self.auto_high_goal_capacity * .01)
        output['auto_fuel_low'] = math.floor(self.auto_low_goal_percentage * self.auto_low_goal_capacity * .01)

        output['climbing'] = "ReadyForTakeoff" if getBoolWithPercentage(self.climb_percentage) else "None"
        output['tele_gear'] = math.floor(self.tele_gear_max * self.tele_gear_consistancy * .01)
        output['tele_fuel_high'] = math.floor(self.tele_high_goal_percentage * self.tele_high_goal_capacity * .01)
        output['tele_fuel_low'] = math.floor(self.tele_low_goal_percentage * self.tele_low_goal_capacity * .01)

        output['foul_percentage'] = 1 if getBoolWithPercentage(self.foul_percentage) else 0
        output['tech_foul_percentage'] = 1 if getBoolWithPercentage(self.tech_foul_percentage) else 0

        return output

