import operator
from Scouting2016.model.reusable_models import Team, Match, OfficialMatch, TeamPictures, TeamComments, TeamCompetesIn, Competition
from Scouting2016.model.models2016 import get_team_metrics, get_defense_stats, \
    get_advanced_team_metrics, ScoreResult, validate_match
from BaseScouting.views.base_views import *
from django.db.models.aggregates import Avg, Sum


class AddTeamCommentsView2016(BaseAddTeamCommentsView):

    def __init__(self):
        BaseAddTeamCommentsView.__init__(self, Team, TeamComments, 'Scouting2016:view_team')


class AddTeamPictureView2016(BaseAddTeamPictureView):

    def __init__(self):
        BaseAddTeamPictureView.__init__(self, Team, TeamPictures, 'Scouting2016/static', 'Scouting2016/robot_pics', 'Scouting2016:view_team')


class GenGraphView2016(BaseGenGraphView):

    def __init__(self):
        BaseGenGraphView.__init__(self, Team)
