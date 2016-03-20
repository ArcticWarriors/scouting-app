from django.db import models
from django.db.models import Avg, Sum
import sys
from django.template.defaultfilters import default


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
            if  sr.auto_defense == "reach":
                auton_reaches += 1
            elif sr.auto_defense != "no_reach":
                print sr.auto_defense
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


def validate_match(match, official_match):

    red_teams, blue_teams = official_match.get_alliance_teams()

    red_high_goals, red_low_goals, red_defense_crossings, red_defenses_crossed, red_error = __get_alliance_results(match, red_teams)
    blue_high_goals, blue_low_goals, blue_defense_crossings, blue_defenses_crossed, blue_error = __get_alliance_results(match, blue_teams)

    red_actual_defenses = []
    red_actual_defenses.append(official_match.redDefense2Name)
    red_actual_defenses.append(official_match.redDefense3Name)
    red_actual_defenses.append(official_match.redDefense4Name)
    red_actual_defenses.append(official_match.redDefense5Name)

    blue_actual_defenses = []
    blue_actual_defenses.append(official_match.blueDefense2Name)
    blue_actual_defenses.append(official_match.blueDefense3Name)
    blue_actual_defenses.append(official_match.blueDefense4Name)
    blue_actual_defenses.append(official_match.blueDefense5Name)

    unexpected_red_crossings = []
    for exp_def in red_defenses_crossed:
        if exp_def not in red_actual_defenses and exp_def != "low_bar":
            unexpected_red_crossings.append(exp_def)

    unexpected_blue_crossings = []
    for exp_def in blue_defenses_crossed:
        if exp_def not in blue_actual_defenses and exp_def != "low_bar":
            unexpected_blue_crossings.append(exp_def)

    invalid_results = {}

    
    num_results = len(match.scoreresult_set.all())
    if num_results != 6:
        invalid_results["Team Count"] = (6, num_results)
        

    ###################################
    # Red
    ###################################
    if red_error:
        expected = [team.teamNumber for team in red_teams]
        all_teams = [sr.team.teamNumber for sr in match.scoreresult_set.all()]
        invalid_results["Red Teams"] = (expected, all_teams)

    if red_high_goals != official_match.redTeleBouldersHigh:
        invalid_results["Red High Goals"] = (official_match.redTeleBouldersHigh, red_high_goals, )

    if red_low_goals != official_match.redTeleBouldersLow:
        invalid_results["Red Low Goals"] = (official_match.redTeleBouldersLow, red_low_goals, )

    if red_defense_crossings != official_match.redTeleDefenseCrossings:
        invalid_results["Red Defense Crossings (Tele)"] = (official_match.redTeleDefenseCrossings, red_defense_crossings, )

    if len(unexpected_red_crossings) != 0:
        invalid_results["Red Available Defenses"] = (red_actual_defenses, unexpected_red_crossings)

    ###################################
    # Blue
    ###################################
    if blue_error:
        expected = [team.teamNumber for team in blue_teams]
        all_teams = [sr.team.teamNumber for sr in match.scoreresult_set.all()]
        invalid_results["Blue Teams"] = (expected, all_teams)

    if blue_high_goals != official_match.blueTeleBouldersHigh:
        invalid_results["Blue High Goals"] = (official_match.blueTeleBouldersHigh, blue_high_goals, )

    if blue_low_goals != official_match.blueTeleBouldersLow:
        invalid_results["Blue Low Goals"] = (official_match.blueTeleBouldersLow, blue_low_goals, )
        
    if blue_defense_crossings != official_match.blueTeleDefenseCrossings:
        invalid_results["Blue Defense Crossings (Tele)"] = (official_match.blueTeleDefenseCrossings, blue_defense_crossings, )

    if len(unexpected_blue_crossings) != 0:
        invalid_results["Blue Available Defenses"] = (blue_actual_defenses, unexpected_blue_crossings)
        
    return len(invalid_results) == 0, invalid_results


class ScoreResultMetric:

    def __init__(self, field_name, display_name, default, metric_type=None):
        self.field_name = field_name
        self.display_name = display_name
        self.default = default
        self.metric_type = metric_type

    def __str__(self):
        return "SRMetric: [%s, %s, %s, %s]" % (self.field_name, self.display_name, self.default, self.metric_type)


class Match(models.Model):

    matchNumber = models.IntegerField()

    def __str__(self):
        return "Match %s" % self.matchNumber


class Team(models.Model):

    teamNumber = models.IntegerField()

    bookmark = models.CharField(max_length=1000)
    
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
    teamFirstYear = models.CharField(max_length=3)

    def get_defense_stats(self, stat_map=None):
        """
        Gets the stats for the defenses crossed for the team.  Groups them by category.

        @param stat_map Optional argument for an existing stat map to append.  Useful when you are getting stats for a whole alliance

        @return The filled out (or updated) stat map
        """

        if stat_map == None:
            stat_map = {}

        no_results = len(self.scoreresult_set.all()) == 0
        print "no results: %s" % no_results

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
                    stat_map[category][defense] += self.scoreresult_set.aggregate(Sum(defense))[defense + "__sum"]

        return stat_map

    def get_average_score(self):
        the_sum = 0
        score_results = self.scoreresult_set.all()

        if len(score_results) == 0:
            return 0
        else:
            for sr in score_results:
                the_sum += sr.calculate_total_score()

            return the_sum / len(score_results)

    def get_metrics(self):
        metrics = self.scoreresult_set.aggregate(Avg("auto_score_low"),
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

    def __str__(self):
        return "Team %s" % self.teamNumber


class TeamComments(models.Model):

    comment = models.CharField(max_length=1000)

    team = models.ForeignKey(Team)


class TeamPictures(models.Model):

    path = models.CharField(max_length=1000)

    team = models.ForeignKey(Team)


class OfficialMatch(models.Model):

    matchNumber = models.IntegerField()
    hasOfficialData = models.BooleanField(default=False)

    redTeam1 = models.ForeignKey(Team, related_name='red1')
    redTeam2 = models.ForeignKey(Team, related_name='red2')
    redTeam3 = models.ForeignKey(Team, related_name='red3')
    blueTeam1 = models.ForeignKey(Team, related_name='blue1')
    blueTeam2 = models.ForeignKey(Team, related_name='blue2')
    blueTeam3 = models.ForeignKey(Team, related_name='blue3')

    redAutonA = models.CharField(max_length=20, default='None')
    redAutonB = models.CharField(max_length=20, default='None')
    redAutonC = models.CharField(max_length=20, default='None')
    redAutoBouldersLow = models.IntegerField(default=-1)
    redAutoBouldersHigh = models.IntegerField(default=-1)
    redTeleBouldersLow = models.IntegerField(default=-1)
    redTeleBouldersHigh = models.IntegerField(default=-1)
    redTeleDefenseCrossings = models.IntegerField(default=-1)
    redDefense1Crossings = models.IntegerField(default=-1)
    redDefense2Name = models.CharField(max_length=20, default='Unspecified')
    redDefense2Crossings = models.IntegerField(default=-1)
    redDefense3Name = models.CharField(max_length=20, default='Unspecified')
    redDefense3Crossings = models.IntegerField(default=-1)
    redDefense4Name = models.CharField(max_length=20, default='Unspecified')
    redDefense4Crossings = models.IntegerField(default=-1)
    redDefense5Name = models.CharField(max_length=20, default='Unspecified')
    redDefense5Crossings = models.IntegerField(default=-1)
    redTowerFaceA = models.CharField(max_length=20, default='none')
    redTowerFaceB = models.CharField(max_length=20, default='none')
    redTowerFaceC = models.CharField(max_length=20, default='none')
    redFouls = models.IntegerField(default=-1)
    redTechFouls = models.IntegerField(default=-1)

    blueAutonA = models.CharField(max_length=20, default='None')
    blueAutonB = models.CharField(max_length=20, default='None')
    blueAutonC = models.CharField(max_length=20, default='None')
    blueAutoBouldersLow = models.IntegerField(default=-1)
    blueAutoBouldersHigh = models.IntegerField(default=-1)
    blueTeleBouldersLow = models.IntegerField(default=-1)
    blueTeleBouldersHigh = models.IntegerField(default=-1)
    blueTeleDefenseCrossings = models.IntegerField(default=-1)
    blueDefense1Crossings = models.IntegerField(default=-1)
    blueDefense2Name = models.CharField(max_length=20, default='Unspecified')
    blueDefense2Crossings = models.IntegerField(default=-1)
    blueDefense3Name = models.CharField(max_length=20, default='Unspecified')
    blueDefense3Crossings = models.IntegerField(default=-1)
    blueDefense4Name = models.CharField(max_length=20, default='Unspecified')
    blueDefense4Crossings = models.IntegerField(default=-1)
    blueDefense5Name = models.CharField(max_length=20, default='Unspecified')
    blueDefense5Crossings = models.IntegerField(default=-1)
    blueTowerFaceA = models.CharField(max_length=20, default='none')
    blueTowerFaceB = models.CharField(max_length=20, default='none')
    blueTowerFaceC = models.CharField(max_length=20, default='none')
    blueFouls = models.IntegerField(default=-1)
    blueTechFouls = models.IntegerField(default=-1)

    audienceSelectionCategory = models.CharField(max_length=1, default='A')

    def get_alliance_teams(self):
        red_teams = []
        blue_teams = []

        red_teams.append(self.redTeam1)
        red_teams.append(self.redTeam2)
        red_teams.append(self.redTeam3)

        blue_teams.append(self.blueTeam1)
        blue_teams.append(self.blueTeam2)
        blue_teams.append(self.blueTeam3)

        return red_teams, blue_teams

    def predict_score(self):
        red_score = 0
        blue_score = 0

        red_score += self.redTeam1.get_average_score()
        red_score += self.redTeam2.get_average_score()
        red_score += self.redTeam3.get_average_score()

        blue_score += self.blueTeam1.get_average_score()
        blue_score += self.blueTeam2.get_average_score()
        blue_score += self.blueTeam3.get_average_score()

        return red_score, blue_score

    def __str__(self):
        output = ""
        output += "Official Match #%s\n" % self.matchNumber

        attributes = sorted(self.__dict__)
        attributes.remove("_state")
        attributes.remove("id")
        for attr_name in attributes:
            value = getattr(self, attr_name)
            output += "  {0:25} = {1}\n".format(attr_name, value)

        return output


class ScoreResult(models.Model):

    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)

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
        output['auto_score_high'] = ScoreResultMetric('auto_score_high', 'Auto High Goals', 0, "Average")
        output['auto_score_low'] = ScoreResultMetric('auto_score_low', 'Auto Low Goals', 0, "Average")
        output['auto_defense'] = ScoreResultMetric('auto_defense', 'Auto Defense', 'no_reach', 0)
        output['auto_spy'] = ScoreResultMetric('auto_spy', 'no', 0)

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
        output['draw_bridge'] = ScoreResultMetric('draw_bridge', 'Draw Bridge Crosses', 0, "Sum")
        output['sally_port'] = ScoreResultMetric('sally_port', 'Sally Port Crosses', 0, "Sum")
        output['rock_wall'] = ScoreResultMetric('rock_wall', 'Rock Wall Crosses', 0, "Sum")
        output['rough_terrain'] = ScoreResultMetric('rough_terrain', 'Rough Terrain Crosses', 0, "Sum")
        output['low_bar'] = ScoreResultMetric('low_bar', 'Low Bar Crosses', 0, "Sum")

        # Defense Speed
        output['slow_fast_portcullis'] = ScoreResultMetric('slow_fast_portcullis', 'Portcullis Speed', 'no_move')
        output['slow_fast_cheval_de_frise'] = ScoreResultMetric('slow_fast_cheval_de_frise', 'Portcullis Speed', 'no_move')
        output['slow_fast_moat'] = ScoreResultMetric('slow_fast_moat', 'Portcullis Speed', 'no_move')
        output['slow_fast_ramparts'] = ScoreResultMetric('slow_fast_ramparts', 'Portcullis Speed', 'no_move')
        output['slow_fast_draw_bridge'] = ScoreResultMetric('slow_fast_draw_bridge', 'Portcullis Speed', 'no_move')
        output['slow_fast_sally_port'] = ScoreResultMetric('slow_fast_sally_port', 'Portcullis Speed', 'no_move')
        output['slow_fast_rock_wall'] = ScoreResultMetric('slow_fast_rock_wall', 'Portcullis Speed', 'no_move')
        output['slow_fast_rough_terrain'] = ScoreResultMetric('slow_fast_rough_terrain', 'Portcullis Speed', 'no_move')
        output['slow_fast_low_bar'] = ScoreResultMetric('slow_fast_low_bar', 'Portcullis Speed', 'no_move')

        # Scale
        output['scale_challenge'] = ScoreResultMetric('scale_challenge', 'Portcullis Speed', 'no')

        # General
        output['notes_text_area'] = ScoreResultMetric('notes_text_area', 'Notes', "")
        output['score_tech_foul'] = ScoreResultMetric('score_tech_foul', 'Tech Fouls', 0, "Sum")

        return output

    def __str__(self):
        output = "Score Result:\n"

        attributes = sorted(self.get_fields().keys())
        for attr_name in attributes:
            value = getattr(self, attr_name)
            output += "  {0:25} = {1}\n".format(attr_name, value)

        return output
