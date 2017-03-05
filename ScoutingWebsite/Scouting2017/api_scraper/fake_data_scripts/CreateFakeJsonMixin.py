import collections
import math


class CreateFakeJsonMixin():

    def _count_mobility(self, robot1_mobility, robot2_mobility, robot3_mobility):
        mobility_sum = 0

        mobility_sum += 1 if robot1_mobility == "Mobility" else 0
        mobility_sum += 1 if robot2_mobility == "Mobility" else 0
        mobility_sum += 1 if robot3_mobility == "Mobility" else 0

        return mobility_sum

    def _count_climbing(self, robot1_climbing, robot2_climbing, robot3_climbing):
        climbing_sum = 0

        climbing_sum += 1 if robot1_climbing == "ReadyForTakeoff" else 0
        climbing_sum += 1 if robot2_climbing == "ReadyForTakeoff" else 0
        climbing_sum += 1 if robot3_climbing == "ReadyForTakeoff" else 0

        return climbing_sum

    def _populate_score_breakdown(self, teams):

        robot1sr, robot2sr, robot3sr = teams

        output = collections.OrderedDict()

        autoGearSum = robot1sr['auto_gear'] + robot2sr['auto_gear'] + robot3sr['auto_gear']
        teleGearSum = robot1sr['tele_gear'] + robot2sr['tele_gear'] + robot3sr['tele_gear']

        #############
        # Auto
        #############
        output["robot1Auto"] = robot1sr['auto_mobility']
        output["robot2Auto"] = robot2sr['auto_mobility']
        output["robot3Auto"] = robot3sr['auto_mobility']
        mobility_count = self._count_mobility(output["robot1Auto"], output["robot2Auto"], output["robot3Auto"])

        output["autoFuelLow"] = robot1sr['auto_fuel_low'] + robot2sr['auto_fuel_low'] + robot3sr['auto_fuel_low']
        output["autoFuelHigh"] = robot1sr['auto_fuel_high'] + robot2sr['auto_fuel_high'] + robot3sr['auto_fuel_high']
        auto_fuel_kpa = output["autoFuelHigh"] + output["autoFuelLow"] / 3.0

        output["rotor1Auto"] = 1 if autoGearSum >= 1 else 0
        output["rotor2Auto"] = 1 if autoGearSum >= 3 else 0
        auto_rotor_count = output["rotor1Auto"] + output["rotor2Auto"]

        #############
        # Tele
        #############
        output["teleopFuelLow"] = robot1sr['tele_fuel_low'] + robot2sr['tele_fuel_low'] + robot3sr['tele_fuel_low']
        output["teleopFuelHigh"] = robot1sr['tele_fuel_high'] + robot2sr['tele_fuel_high'] + robot3sr['tele_fuel_high']
        teleop_fuel_kpa = output["teleopFuelLow"] / 3.0 + output["teleopFuelHigh"] / 9.0

        output["rotor1Engaged"] = max(0, (1 if teleGearSum >= 1 else 0) - output["rotor1Auto"])
        output["rotor2Engaged"] = max(0, (1 if teleGearSum >= 3 else 0) - output["rotor2Auto"])
        output["rotor3Engaged"] = 1 if teleGearSum >= 7 else 0
        output["rotor4Engaged"] = 1 if teleGearSum >= 13 else 0
        teleop_rotor_count = output["rotor1Engaged"] + output["rotor2Engaged"] + output["rotor3Engaged"] + output["rotor4Engaged"]

        output["touchpadNear"] = robot1sr['climbing']
        output["touchpadMiddle"] = robot2sr['climbing']
        output["touchpadFar"] = robot3sr['climbing']
        climbing_count = self._count_climbing(output["touchpadNear"], output["touchpadMiddle"], output["touchpadFar"])

        output["foulCount"] = robot1sr['foul_percentage'] + robot2sr['foul_percentage'] + robot3sr['foul_percentage']
        output["techFoulCount"] = robot1sr['tech_foul_percentage'] + robot2sr['tech_foul_percentage'] + robot3sr['tech_foul_percentage']

        #############
        # Sums
        #############
        kpa_sum = math.floor(auto_fuel_kpa + teleop_fuel_kpa)
        output["autoMobilityPoints"] = mobility_count * 5
        output["autoRotorPoints"] = auto_rotor_count * 60
        output["autoPoints"] = output["autoMobilityPoints"] + output["autoRotorPoints"] + math.floor(auto_fuel_kpa)

        output["teleopFuelPoints"] = math.floor(teleop_fuel_kpa)
        output["teleopRotorPoints"] = teleop_rotor_count * 40
        output["teleopTakeoffPoints"] = climbing_count * 50
        output["teleopPoints"] = output["teleopFuelPoints"] + output["teleopRotorPoints"] + output["teleopTakeoffPoints"]

        # TODO: Check the points
        output["foulPoints"] = output["foulCount"] * 5 + output["techFoulCount"] * 25
        output["totalPoints"] = output["autoPoints"] + output["teleopPoints"]

        output["kPaRankingPointAchieved"] = kpa_sum >= 40
        output["rotorRankingPointAchieved"] = (auto_rotor_count + teleop_rotor_count) == 4

        return output
