from django.db import models
from django.db.models import Avg, Sum


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
    homepage = models.CharField(max_length=1000)
    teamOrganized = models.CharField(max_length=1000)
    teamLikeable = models.CharField(max_length=1000)
    teamSwag = models.CharField(max_length=1000)
    teamAwards = models.CharField(max_length=1000)
    teamAbilities = models.CharField(max_length=1000)
    teamAlliances = models.CharField(max_length=1000)
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

        defenses = {}
        defenses['A'] = ('portcullis', 'cheval_de_frise')
        defenses['B'] = ('moat', 'ramparts')
        defenses['C'] = ('draw_bridge', 'sally_port')
        defenses['D'] = ('rock_wall', 'rough_terrain')

        no_results = len(self.scoreresult_set.all()) == 0
        print "no results: %s" % no_results

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

    redTeam1 = models.ForeignKey(Team, related_name='red1')
    redTeam2 = models.ForeignKey(Team, related_name='red2')
    redTeam3 = models.ForeignKey(Team, related_name='red3')
    blueTeam1 = models.ForeignKey(Team, related_name='blue1')
    blueTeam2 = models.ForeignKey(Team, related_name='blue2')
    blueTeam3 = models.ForeignKey(Team, related_name='blue3')

    redAutoBouldersLow = models.IntegerField(default=-1)
    redAutoBouldersHigh = models.IntegerField(default=-1)
    redTeleBouldersLow = models.IntegerField(default=-1)
    redTeleBouldersHigh = models.IntegerField(default=-1)
    redTowerFaceA = models.CharField(max_length=20, default='none')
    redTowerFaceB = models.CharField(max_length=20, default='none')
    redTowerFaceC = models.CharField(max_length=20, default='none')
    redFouls = models.IntegerField(default=-1)
    redTechFouls = models.IntegerField(default=-1)

    blueAutoBouldersLow = models.IntegerField(default=-1)
    blueAutoBouldersHigh = models.IntegerField(default=-1)
    blueTeleBouldersLow = models.IntegerField(default=-1)
    blueTeleBouldersHigh = models.IntegerField(default=-1)
    blueTowerFaceA = models.CharField(max_length=20, default='none')
    blueTowerFaceB = models.CharField(max_length=20, default='none')
    blueTowerFaceC = models.CharField(max_length=20, default='none')
    blueFouls = models.IntegerField(default=-1)
    blueTechFouls = models.IntegerField(default=-1)

    audienceSelectionCategory = models.CharField(max_length=1, default='A')

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
    slow_fast_bridge = models.CharField(max_length=50)
    slow_fast_cheval = models.CharField(max_length=50)
    slow_fast_low_bar = models.CharField(max_length=50)
    slow_fast_moat = models.CharField(max_length=50)
    slow_fast_portcullis = models.CharField(max_length=50)
    slow_fast_ramparts = models.CharField(max_length=50)
    slow_fast_rock_wall = models.CharField(max_length=50)
    slow_fast_rough = models.CharField(max_length=50)
    slow_fast_sally = models.CharField(max_length=50)

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
        output['cheval_de_frise'] = ScoreResultMetric('cheval_de_frise', 'Cheval De Frise Crosses', 0, "Sum")
        output['draw_bridge'] = ScoreResultMetric('draw_bridge', 'Draw Bridge Crosses', 0, "Sum")
        output['low_bar'] = ScoreResultMetric('low_bar', 'Low Bar Crosses', 0, "Sum")
        output['moat'] = ScoreResultMetric('moat', 'Moat Crosses', 0, "Average")
        output['ramparts'] = ScoreResultMetric('ramparts', 'Ramparts Crosses', 0, "Sum")
        output['rock_wall'] = ScoreResultMetric('rock_wall', 'Rock Wall Crosses', 0, "Sum")
        output['rough_terrain'] = ScoreResultMetric('rough_terrain', 'Rough Terrain Crosses', 0, "Sum")
        output['sally_port'] = ScoreResultMetric('sally_port', 'Sally Port Crosses', 0, "Sum")
        output['portcullis'] = ScoreResultMetric('portcullis', 'Portcullis Crosses', 0, "Sum")

        # Defense Speed
        output['slow_fast_bridge'] = ScoreResultMetric('slow_fast_bridge', 'Portcullis Speed', 'no_move')
        output['slow_fast_cheval'] = ScoreResultMetric('slow_fast_cheval', 'Portcullis Speed', 'no_move')
        output['slow_fast_low_bar'] = ScoreResultMetric('slow_fast_low_bar', 'Portcullis Speed', 'no_move')
        output['slow_fast_moat'] = ScoreResultMetric('slow_fast_moat', 'Portcullis Speed', 'no_move')
        output['slow_fast_portcullis'] = ScoreResultMetric('slow_fast_portcullis', 'Portcullis Speed', 'no_move')
        output['slow_fast_ramparts'] = ScoreResultMetric('slow_fast_ramparts', 'Portcullis Speed', 'no_move')
        output['slow_fast_rock_wall'] = ScoreResultMetric('slow_fast_rock_wall', 'Portcullis Speed', 'no_move')
        output['slow_fast_rough'] = ScoreResultMetric('slow_fast_rough', 'Portcullis Speed', 'no_move')
        output['slow_fast_sally'] = ScoreResultMetric('slow_fast_sally', 'Portcullis Speed', 'no_move')

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
