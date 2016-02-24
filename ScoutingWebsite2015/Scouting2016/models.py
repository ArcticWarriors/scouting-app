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

    redTeam1 = models.IntegerField()
    redTeam2 = models.IntegerField()
    redTeam3 = models.IntegerField()
    blueTeam1 = models.IntegerField()
    blueTeam2 = models.IntegerField()
    blueTeam3 = models.IntegerField()

    redScore = models.IntegerField(default=-1)
    blueScore = models.IntegerField(default=-1)




class ScoreResult(models.Model):

    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)

    auto_score_low = models.IntegerField()
    auto_score_high = models.IntegerField()

    cheval_de_frise = models.IntegerField()
    ramparts = models.IntegerField()
    sally_port = models.IntegerField()
    low_bar = models.IntegerField()
    rock_wall = models.IntegerField()
    draw_bridge = models.IntegerField()
    moat = models.IntegerField()
    rough_terrain = models.IntegerField()
    portcullis = models.IntegerField(default=0)

    score_tech_foul = models.IntegerField()

    high_score_fail = models.IntegerField()
    high_score_successful = models.IntegerField()
    low_score_successful = models.IntegerField()
    low_score_fail = models.IntegerField()

    notes_text_area = models.CharField(max_length=1000)

    # new stuff below
    auto_defense = models.CharField(max_length=50, default="")
    auto_spy = models.CharField(max_length=50, default="")

    scale_challenge = models.CharField(max_length=50, default="")

    slow_fast_bridge = models.CharField(max_length=50, default="")
    slow_fast_cheval = models.CharField(max_length=50, default="")
    slow_fast_low_bar = models.CharField(max_length=50, default="")
    slow_fast_moat = models.CharField(max_length=50, default="")
    slow_fast_portcullis = models.CharField(max_length=50, default="")
    slow_fast_ramparts = models.CharField(max_length=50, default="")
    slow_fast_rock_wall = models.CharField(max_length=50, default="")
    slow_fast_rough = models.CharField(max_length=50, default="")
    slow_fast_sally = models.CharField(max_length=50, default="")

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
