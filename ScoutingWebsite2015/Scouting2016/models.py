from django.db import models
from django.db.models import Avg, Sum


class Match(models.Model):

    matchNumber = models.IntegerField()

    def __str__(self):
        return "Match %s" % self.matchNumber


class Team(models.Model):

    teamNumber = models.IntegerField()

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
    def get_fields_with_defaults():

        output = {}

        output['auto_score_high'] = 0
        output['auto_score_low'] = 0
        output['cheval_de_frise'] = 0
        output['draw_bridge'] = 0
        output['high_score_fail'] = 0
        output['high_score_successful'] = 0
        output['low_bar'] = 0
        output['low_score_fail'] = 0
        output['low_score_successful'] = 0
        output['moat'] = 0
        output['notes_text_area'] = 0
        output['ramparts'] = 0
        output['rock_wall'] = 0
        output['rough_terrain'] = 0
        output['score_tech_foul'] = 0
        output['sally_port'] = 0
        output['portcullis'] = 0
        output['auto_spy'] = 'yes'
        output['auto_defense'] = 'no_reach'
        output['scale_challenge'] = 'no'
        output['slow_fast_bridge'] = 'no_move'
        output['slow_fast_cheval'] = 'no_move'
        output['slow_fast_low_bar'] = 'no_move'
        output['slow_fast_moat'] = 'no_move'
        output['slow_fast_portcullis'] = 'no_move'
        output['slow_fast_ramparts'] = 'no_move'
        output['slow_fast_rock_wall'] = 'no_move'
        output['slow_fast_rough'] = 'no_move'
        output['slow_fast_sally'] = 'no_move'

        return output

    def __str__(self):
        output = "Score Result:\n"

        attributes = sorted(self.get_fields_with_defaults().keys())
        for attr_name in attributes:
            value = getattr(self, attr_name)
            output += "  {0:25} = {1}\n".format(attr_name, value)

        return output
