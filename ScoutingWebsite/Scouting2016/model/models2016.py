'''
Created on Mar 28, 2016

@author: PJ
'''
from django.db.models.aggregates import Avg, Sum
from django.db import models
from Scouting2016.model.reusable_models import ScoreResultMetric, Team, \
    OfficialMatch, Match, Competition


def __get_alliance_results(match, teams,):
    high_goals = 0
    low_goals = 0
    defense_crossing = 0
    defenses_crossed = set()
    auton_crossings = 0
    auton_reaches = 0

    error = False
    for team in teams:
        sr_search = match.scoreresult_set.filter(team__teamNumber=team.teamNumber)
        if len(sr_search) != 0:
            sr = sr_search[0]
            high_goals += sr.high_score_successful
            low_goals += sr.low_score_successful
            if sr.auto_defense == "reach":
                auton_reaches += 1
            elif sr.auto_defense != "no_reach":
                print(sr.auto_defense)
                auton_crossings += 1

            for defense in get_flat_defenses():
                value = getattr(sr, defense)
                if value != 0:
                    defenses_crossed.add(defense)
                    defense_crossing += value
        else:
            error = True

    defense_crossing -= auton_crossings

    return high_goals, low_goals, defense_crossing, defenses_crossed, error


def get_defenses():

    defenses = {}
    defenses['A'] = ('portcullis', 'cheval_de_frise')
    defenses['B'] = ('moat', 'ramparts')
    defenses['C'] = ('draw_bridge', 'sally_port')
    defenses['D'] = ('rock_wall', 'rough_terrain')

    return defenses


def get_flat_defenses():
    grouped_defenses = get_defenses()

    flat_defense = ['low_bar']

    for category in grouped_defenses:
        for defense in grouped_defenses[category]:
            flat_defense.append(defense)

    return flat_defense


def get_defense_stats(team, stat_map=None):
    """
    Gets the stats for the defenses crossed for the team.  Groups them by category.
    @param stat_map Optional argument for an existing stat map to append.  Useful when you are getting stats for a whole alliance
    @return The filled out (or updated) stat map
    """

    if stat_map == None:
        stat_map = {}

    no_results = len(team.scoreresult_set.all()) == 0
    print("no results: %s" % no_results)

    defenses = get_defenses()

    for category in defenses:

        if category not in stat_map:
            stat_map[category] = {}

        for defense in defenses[category]:
            if defense not in stat_map[category]:
                stat_map[category][defense] = 0

            if no_results:
                stat_map[category][defense] += 0
            else:
                stat_map[category][defense] += team.scoreresult_set.aggregate(Sum(defense))[defense + "__sum"]

    return stat_map


def get_team_metrics(team):
    metrics = team.scoreresult_set.aggregate(Avg("auto_score_low"),
                                             Avg("auto_score_high"),

                                             Sum("cheval_de_frise"),
                                             Sum("ramparts"),
                                             Sum("sally_port"),
                                             Sum("low_bar"),
                                             Sum("rock_wall"),
                                             Sum("draw_bridge"),
                                             Sum("moat"),
                                             Sum("rough_terrain"),
                                             Sum("portcullis"),

                                             Sum("score_tech_foul"),
                                             Avg("high_score_fail"),
                                             Avg("high_score_successful"),
                                             Avg("low_score_fail"),
                                             Avg("low_score_successful"),
                                             )

    # Format all of the numbers.  If we haven't scouted the team, None will be returned.  Turn that into NA
    for key in metrics:
        if metrics[key] == None:
            metrics[key] = "NA"
        elif "__avg" in key:
            metrics[key] = "{:10.2f}".format(metrics[key])

    return metrics


class TeamPitScouting(models.Model):

    team = models.OneToOneField(Team)

    bookmark = models.CharField(max_length=1000, default="no")

    teamOrganized = models.CharField(max_length=1000)
    teamLikeable = models.CharField(max_length=1000)
    teamSwag = models.CharField(max_length=1000)
    teamAwards = models.CharField(max_length=1000)
    teamAlliances = models.CharField(max_length=1000, default="no")

    drive = models.CharField(max_length=1000, default="no")
    Auto = models.CharField(max_length=1000, default="no")
    ScoreHigh = models.CharField(max_length=1000, default="no")
    ScoreLow = models.CharField(max_length=1000, default="no")
    portcullis = models.CharField(max_length=1000, default="no")
    cheval = models.CharField(max_length=1000, default="no")
    moat = models.CharField(max_length=1000, default="no")
    ramparts = models.CharField(max_length=1000, default="no")
    sally = models.CharField(max_length=1000, default="no")
    drawbridge = models.CharField(max_length=1000, default="no")
    rockwall = models.CharField(max_length=1000, default="no")
    rough = models.CharField(max_length=1000, default="no")
    lowBar = models.CharField(max_length=1000, default="no")
    scale = models.CharField(max_length=1000, default="no")

    teamAlly174 = models.CharField(max_length=3)
    teamOperational = models.CharField(max_length=3)
    teamOperationProblems = models.CharField(max_length=1000)

#     audienceSelectionCategory = models.CharField(max_length=1, default='A')

#     def get_alliance_teams(self):
#         red_teams = []
#         blue_teams = []
#
#         red_teams.append(self.redTeam1)
#         red_teams.append(self.redTeam2)
#         red_teams.append(self.redTeam3)
#
#         blue_teams.append(self.blueTeam1)
#         blue_teams.append(self.blueTeam2)
#         blue_teams.append(self.blueTeam3)
#
#         return red_teams, blue_teams
#
#     def predict_score(self):
#         red_score = 0
#         blue_score = 0
#
#         red_score += self.redTeam1.get_average_score()
#         red_score += self.redTeam2.get_average_score()
#         red_score += self.redTeam3.get_average_score()
#
#         blue_score += self.blueTeam1.get_average_score()
#         blue_score += self.blueTeam2.get_average_score()
#         blue_score += self.blueTeam3.get_average_score()
#
#         return red_score, blue_score
#
#     def __str__(self):
#         output = ""
#         output += "Official Match #%s\n" % self.matchNumber
#
#         attributes = sorted(self.__dict__)
#         attributes.remove("_state")
#         attributes.remove("id")
#         for attr_name in attributes:
#             value = getattr(self, attr_name)
#             output += "  {0:25} = {1}\n".format(attr_name, value)
#
#         return output


class OfficialMatchScoreResult(models.Model):

    official_match = models.ForeignKey(OfficialMatch)
    competition = models.ForeignKey(Competition)

    team1 = models.ForeignKey(Team, related_name='da_team1')
    team2 = models.ForeignKey(Team, related_name='da_team2')
    team3 = models.ForeignKey(Team, related_name='da_team3')

    autonA = models.CharField(max_length=20, default='None')
    autonB = models.CharField(max_length=20, default='None')
    autonC = models.CharField(max_length=20, default='None')
    autoBouldersLow = models.IntegerField(default=-1)
    autoBouldersHigh = models.IntegerField(default=-1)
    teleBouldersLow = models.IntegerField(default=-1)
    teleBouldersHigh = models.IntegerField(default=-1)
    teleDefenseCrossings = models.IntegerField(default=-1)
    defense1Crossings = models.IntegerField(default=-1)
    defense2Name = models.CharField(max_length=20, default='Unspecified')
    defense2Crossings = models.IntegerField(default=-1)
    defense3Name = models.CharField(max_length=20, default='Unspecified')
    defense3Crossings = models.IntegerField(default=-1)
    defense4Name = models.CharField(max_length=20, default='Unspecified')
    defense4Crossings = models.IntegerField(default=-1)
    defense5Name = models.CharField(max_length=20, default='Unspecified')
    defense5Crossings = models.IntegerField(default=-1)
    towerFaceA = models.CharField(max_length=20, default='none')
    towerFaceB = models.CharField(max_length=20, default='none')
    towerFaceC = models.CharField(max_length=20, default='none')
    fouls = models.IntegerField(default=-1)
    techFouls = models.IntegerField(default=-1)

    def predict(self):
        return 123


class ScoreResult(models.Model):

    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)
    competition = models.ForeignKey(Competition)

    # Auton
    auto_defense = models.CharField(max_length=50)
    auto_spy = models.CharField(max_length=50)
    auto_score_low = models.IntegerField()
    auto_score_high = models.IntegerField()

    # Ball Manipulation
    high_score_fail = models.IntegerField()
    high_score_successful = models.IntegerField()
    low_score_fail = models.IntegerField()
    low_score_successful = models.IntegerField()

    # Defense Crosses
    portcullis = models.IntegerField()
    cheval_de_frise = models.IntegerField()
    moat = models.IntegerField()
    ramparts = models.IntegerField()
    draw_bridge = models.IntegerField()
    sally_port = models.IntegerField()
    rock_wall = models.IntegerField()
    rough_terrain = models.IntegerField()
    low_bar = models.IntegerField()

    # Defense Cross Speed
    slow_fast_portcullis = models.CharField(max_length=50)
    slow_fast_cheval_de_frise = models.CharField(max_length=50)
    slow_fast_moat = models.CharField(max_length=50)
    slow_fast_ramparts = models.CharField(max_length=50)
    slow_fast_draw_bridge = models.CharField(max_length=50)
    slow_fast_sally_port = models.CharField(max_length=50)
    slow_fast_rock_wall = models.CharField(max_length=50)
    slow_fast_rough_terrain = models.CharField(max_length=50)
    slow_fast_low_bar = models.CharField(max_length=50)

    # General
    scale_challenge = models.CharField(max_length=50)
    score_tech_foul = models.IntegerField()

    # Comments
    notes_text_area = models.CharField(max_length=1000)

    def calculate_auton_score(self):
        total = 0
        total += (5 * self.auto_score_low)
        total += (10 * self.auto_score_high)

        if self.auto_defense == 'reached':
            total += 2
        elif self.auto_defense != 'no_reach':
            total += 10

        return total

    def calculate_teleop_no_defense(self):
        total = 0
        total += (5 * self.high_score_successful)
        total += (2 * self.low_score_successful)

        if self.scale_challenge == 'scale':
            total += 15
        elif self.scale_challenge == "challenge":
            total += 5

        total -= (3 * self.score_tech_foul)

        return total

    def calculate_raw_defense_score(self):
        total = 0

        total += 5 * self.portcullis
        total += 5 * self.cheval_de_frise
        total += 5 * self.moat
        total += 5 * self.ramparts
        total += 5 * self.draw_bridge
        total += 5 * self.sally_port
        total += 5 * self.rock_wall
        total += 5 * self.rough_terrain
        total += 5 * self.low_bar

        return total

    def calculate_capped_defense_score(self):
        total = 0

        total += 5 * max(2, self.portcullis)
        total += 5 * max(2, self.cheval_de_frise)
        total += 5 * max(2, self.moat)
        total += 5 * max(2, self.ramparts)
        total += 5 * max(2, self.draw_bridge)
        total += 5 * max(2, self.sally_port)
        total += 5 * max(2, self.rock_wall)
        total += 5 * max(2, self.rough_terrain)
        total += 5 * max(2, self.low_bar)

        return total

    def calculate_total_score(self):
        total = 0
        total += self.calculate_auton_score()
        total += self.calculate_teleop_no_defense()
        total += self.calculate_capped_defense_score()

        return total

    @staticmethod
    def get_fields():

        output = {}

        # Auto
        output['auto_defense'] = ScoreResultMetric('auto_defense', 'Auto Defense', 'no_reach')
        output['auto_spy'] = ScoreResultMetric('auto_spy', 'Spy Bot', 'no')
        output['auto_score_high'] = ScoreResultMetric('auto_score_high', 'Auto High Goals', 0, "Average")
        output['auto_score_low'] = ScoreResultMetric('auto_score_low', 'Auto Low Goals', 0, "Average")

        # Boulders
        output['high_score_fail'] = ScoreResultMetric('high_score_fail', 'High Misses', 0, "Average")
        output['high_score_successful'] = ScoreResultMetric('high_score_successful', 'High Goals', 0, "Average")
        output['low_score_fail'] = ScoreResultMetric('low_score_fail', 'Low Misses', 0, "Average")
        output['low_score_successful'] = ScoreResultMetric('low_score_successful', 'Low Goals', 0, "Average")

        # Defenses Crossed
        output['portcullis'] = ScoreResultMetric('portcullis', 'Portcullis Crosses', 0, "Sum")
        output['cheval_de_frise'] = ScoreResultMetric('cheval_de_frise', 'Cheval De Frise Crosses', 0, "Sum")
        output['moat'] = ScoreResultMetric('moat', 'Moat Crosses', 0, "Average")
        output['ramparts'] = ScoreResultMetric('ramparts', 'Ramparts Crosses', 0, "Sum")
        output['draw_bridge'] = ScoreResultMetric('draw_bridge', 'Drawbridge Crosses', 0, "Sum")
        output['sally_port'] = ScoreResultMetric('sally_port', 'Sally Port Crosses', 0, "Sum")
        output['rock_wall'] = ScoreResultMetric('rock_wall', 'Rock Wall Crosses', 0, "Sum")
        output['rough_terrain'] = ScoreResultMetric('rough_terrain', 'Rough Terrain Crosses', 0, "Sum")
        output['low_bar'] = ScoreResultMetric('low_bar', 'Low Bar Crosses', 0, "Sum")

        # Defense Speed
        output['slow_fast_portcullis'] = ScoreResultMetric('slow_fast_portcullis', 'Portcullis Speed', 'no_move')
        output['slow_fast_cheval_de_frise'] = ScoreResultMetric('slow_fast_cheval_de_frise', 'Cheval de Frise Speed', 'no_move')
        output['slow_fast_moat'] = ScoreResultMetric('slow_fast_moat', 'Moat Speed', 'no_move')
        output['slow_fast_ramparts'] = ScoreResultMetric('slow_fast_ramparts', 'Ramparts Speed', 'no_move')
        output['slow_fast_draw_bridge'] = ScoreResultMetric('slow_fast_draw_bridge', 'Drawbridge Speed', 'no_move')
        output['slow_fast_sally_port'] = ScoreResultMetric('slow_fast_sally_port', 'Sally Port Speed', 'no_move')
        output['slow_fast_rock_wall'] = ScoreResultMetric('slow_fast_rock_wall', 'Rock Wall Speed', 'no_move')
        output['slow_fast_rough_terrain'] = ScoreResultMetric('slow_fast_rough_terrain', 'Rough Terrain Speed', 'no_move')
        output['slow_fast_low_bar'] = ScoreResultMetric('slow_fast_low_bar', 'Low Bar Speed', 'no_move')

        # General
        output['scale_challenge'] = ScoreResultMetric('scale_challenge', 'Scale Channenge', 'no')
        output['score_tech_foul'] = ScoreResultMetric('score_tech_foul', 'Tech Fouls', 0, "Sum")

        # Comments
        output['notes_text_area'] = ScoreResultMetric('notes_text_area', 'Notes', "")

        return output

    def __str__(self):
        output = "Score Result:\n"

        attributes = sorted(self.get_fields().keys())
        for attr_name in attributes:
            value = getattr(self, attr_name)
            output += "  {0:25} = {1}\n".format(attr_name, value)

        return output


def get_advanced_team_metrics(team, all_fields=ScoreResult.get_fields()):

    kargs = {}
    field_order = []
    for key in all_fields:
        sr_field = all_fields[key]
        field_order.append(sr_field.display_name)
        if sr_field.metric_type == "Average":
            kargs[sr_field.display_name] = Avg(key)
        elif sr_field.metric_type == "Sum":
            kargs[sr_field.display_name] = Sum(key)
        else:
            print("field %s is not metrics-able" % key)

    results = team.scoreresult_set.aggregate(**kargs)
    output = []
    for key in all_fields:
        sr_field = all_fields[key]
        if sr_field.display_name in results:
            print type(results[sr_field.display_name])
            result = results[sr_field.display_name]
            if type(result) == float:
                result = "%.2f" % result
            output.append((sr_field.display_name, result))

    return output
