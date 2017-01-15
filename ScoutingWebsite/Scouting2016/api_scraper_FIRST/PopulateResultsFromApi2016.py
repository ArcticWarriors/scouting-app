'''
Created on Mar 8, 2016

@author: PJ
'''

from BaseScouting.api_scraper_FIRST.PopulateResultsFromApi import PopulateRegionalResults


class PopulateRegionalresults2016(PopulateRegionalResults):

    def __init__(self):
        from Scouting2016.model import Team, Compitition, OfficialMatch, OfficialMatchScoreResult
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

        official_match_sr.autoBouldersLow = alliance_info["autoBouldersLow"]
        official_match_sr.autoBouldersHigh = alliance_info["autoBouldersHigh"]
        official_match_sr.teleBouldersLow = alliance_info["teleopBouldersLow"]
        official_match_sr.teleBouldersHigh = alliance_info["teleopBouldersHigh"]
        official_match_sr.teleDefenseCrossings = alliance_info["teleopCrossingPoints"] / 5.0
        official_match_sr.autonA = alliance_info["robot1Auto"] if alliance_info["robot1Auto"] != None else "None"
        official_match_sr.autonB = alliance_info["robot2Auto"] if alliance_info["robot2Auto"] != None else "None"
        official_match_sr.autonC = alliance_info["robot3Auto"] if alliance_info["robot3Auto"] != None else "None"
        official_match_sr.towerFaceA = alliance_info["towerFaceA"]
        official_match_sr.towerFaceB = alliance_info["towerFaceB"]
        official_match_sr.towerFaceC = alliance_info["towerFaceC"]
        official_match_sr.fouls = alliance_info["foulCount"]
        official_match_sr.techFouls = alliance_info["techFoulCount"]

        official_match_sr.defense2Name = self.defense_name_lookup[alliance_info["position2"]]
        official_match_sr.defense3Name = self.defense_name_lookup[alliance_info["position3"]]
        official_match_sr.defense4Name = self.defense_name_lookup[alliance_info["position4"]]
        official_match_sr.defense5Name = self.defense_name_lookup[alliance_info["position5"]]
        official_match_sr.defense1Crossings = alliance_info["position1crossings"]
        official_match_sr.defense2Crossings = alliance_info["position2crossings"]
        official_match_sr.defense3Crossings = alliance_info["position3crossings"]
        official_match_sr.defense4Crossings = alliance_info["position4crossings"]
        official_match_sr.defense5Crossings = alliance_info["position5crossings"]

        official_match_sr.save()
