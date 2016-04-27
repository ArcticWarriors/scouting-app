'''
Created on Mar 8, 2016

@author: PJ
'''

from BaseScouting.api_scraper.PopulateResultsFromApi import PopulateRegionalResults


class PopulateRegionalResults2015(PopulateRegionalResults):

    def __init__(self):
        from Scouting2015.model import Team, Compitition, OfficialMatch, OfficialMatchScoreResult
        PopulateRegionalResults.__init__(self, Team, Compitition, OfficialMatch, OfficialMatchScoreResult)

        self.defense_name_lookup = {}
        self.defense_name_lookup["A_Portcullis"] = "portcullis"
        self.defense_name_lookup["A_ChevalDeFrise"] = "cheval_de_frise"
        self.defense_name_lookup["B_Moat"] = "moat"
        self.defense_name_lookup["B_Ramparts"] = "ramparts"
        self.defense_name_lookup["C_Drawbridge"] = "draw_bridge"
        self.defense_name_lookup["C_SallyPort"] = "sally_port"
        self.defense_name_lookup["D_RockWall"] = "rock_wall"
        self.defense_name_lookup["D_RoughTerrain"] = "rough_terrain"
        self.defense_name_lookup["NotSpecified"] = "NA"

    def populate_official_sr(self, official_match_sr, alliance_info):
        pass

        # Auton
        official_match_sr.auton_robot_set = alliance_info["robotSet"]
        official_match_sr.auton_tote_set = alliance_info["toteSet"]
        official_match_sr.auton_tote_stack = alliance_info["toteStack"]
        official_match_sr.auton_container_set = alliance_info["containerSet"]

        # Totes
        official_match_sr.totes_on_close_platform = alliance_info["toteCountNear"]
        official_match_sr.totes_on_far_platform = alliance_info["toteCountFar"]

        # Containers
        official_match_sr.containers_on_level_1 = alliance_info["containerCountLevel1"]
        official_match_sr.containers_on_level_2 = alliance_info["containerCountLevel2"]
        official_match_sr.containers_on_level_3 = alliance_info["containerCountLevel3"]
        official_match_sr.containers_on_level_4 = alliance_info["containerCountLevel4"]
        official_match_sr.containers_on_level_5 = alliance_info["containerCountLevel5"]
        official_match_sr.containers_on_level_6 = alliance_info["containerCountLevel6"]

        official_match_sr.save()
