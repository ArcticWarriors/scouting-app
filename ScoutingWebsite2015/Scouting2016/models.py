
from Scouting2016.model.reusable_models import Match, OfficialMatch, Team, TeamComments, TeamPictures, ScoreResultMetric
from Scouting2016.model.models2016 import TeamPitScouting, OfficialMatchScoreResult, ScoreResult



# def validate_match(match, official_match):
#
#     print official_match.officialmatchscoreresult_set.all()
#
#     red_teams, blue_teams = official_match.get_alliance_teams()
#
#     red_high_goals, red_low_goals, red_defense_crossings, red_defenses_crossed, red_error = __get_alliance_results(match, red_teams)
#     blue_high_goals, blue_low_goals, blue_defense_crossings, blue_defenses_crossed, blue_error = __get_alliance_results(match, blue_teams)
#
#     red_actual_defenses = []
#     red_actual_defenses.append(official_match.redDefense2Name)
#     red_actual_defenses.append(official_match.redDefense3Name)
#     red_actual_defenses.append(official_match.redDefense4Name)
#     red_actual_defenses.append(official_match.redDefense5Name)
#
#     blue_actual_defenses = []
#     blue_actual_defenses.append(official_match.blueDefense2Name)
#     blue_actual_defenses.append(official_match.blueDefense3Name)
#     blue_actual_defenses.append(official_match.blueDefense4Name)
#     blue_actual_defenses.append(official_match.blueDefense5Name)
#
#     unexpected_red_crossings = []
#     for exp_def in red_defenses_crossed:
#         if exp_def not in red_actual_defenses and exp_def != "low_bar":
#             unexpected_red_crossings.append(exp_def)
#
#     unexpected_blue_crossings = []
#     for exp_def in blue_defenses_crossed:
#         if exp_def not in blue_actual_defenses and exp_def != "low_bar":
#             unexpected_blue_crossings.append(exp_def)
#
#     invalid_results = {}
#
#     num_results = len(match.scoreresult_set.all())
#     if num_results != 6:
#         invalid_results["Team Count"] = (6, num_results)
#
#     ###################################
#     # Red
#     ###################################
#     if red_error:
#         expected = [team.teamNumber for team in red_teams]
#         all_teams = [sr.team.teamNumber for sr in match.scoreresult_set.all()]
#         invalid_results["Red Teams"] = (expected, all_teams)
#
#     if red_high_goals != official_match.redTeleBouldersHigh:
#         invalid_results["Red High Goals"] = (official_match.redTeleBouldersHigh, red_high_goals, )
#
#     if red_low_goals != official_match.redTeleBouldersLow:
#         invalid_results["Red Low Goals"] = (official_match.redTeleBouldersLow, red_low_goals, )
#
#     if red_defense_crossings != official_match.redTeleDefenseCrossings:
#         invalid_results["Red Defense Crossings (Tele)"] = (official_match.redTeleDefenseCrossings, red_defense_crossings, )
#
#     if len(unexpected_red_crossings) != 0:
#         invalid_results["Red Available Defenses"] = (red_actual_defenses, unexpected_red_crossings)
#
#     ###################################
#     # Blue
#     ###################################
#     if blue_error:
#         expected = [team.teamNumber for team in blue_teams]
#         all_teams = [sr.team.teamNumber for sr in match.scoreresult_set.all()]
#         invalid_results["Blue Teams"] = (expected, all_teams)
#
#     if blue_high_goals != official_match.blueTeleBouldersHigh:
#         invalid_results["Blue High Goals"] = (official_match.blueTeleBouldersHigh, blue_high_goals, )
#
#     if blue_low_goals != official_match.blueTeleBouldersLow:
#         invalid_results["Blue Low Goals"] = (official_match.blueTeleBouldersLow, blue_low_goals, )
#
#     if blue_defense_crossings != official_match.blueTeleDefenseCrossings:
#         invalid_results["Blue Defense Crossings (Tele)"] = (official_match.blueTeleDefenseCrossings, blue_defense_crossings, )
#
#     if len(unexpected_blue_crossings) != 0:
#         invalid_results["Blue Available Defenses"] = (blue_actual_defenses, unexpected_blue_crossings)
#
#     return len(invalid_results) == 0, invalid_results



