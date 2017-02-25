
from Scouting2013.model.reusable_models import Team, Match, OfficialMatch, TeamPictures, TeamComments, TeamCompetesIn, Competition
from Scouting2013.model.models2013 import ScoreResult, get_team_metrics
from BaseScouting.views.base_views import BaseAddTeamCommentsView, \
    BaseAddTeamPictureView, BaseAllTeamsViews, BaseSingleTeamView, \
    BaseAllMatchesView, BaseSingleMatchView, BaseMatchPredictionView, \
    BaseGenGraphView, BaseHomepageView
from django.db.models.aggregates import Avg, Sum


class HomepageView2013(BaseHomepageView):

    def __init__(self):
        BaseHomepageView.__init__(self, Competition, 'Scouting2013/index.html')

    def get_our_metrics(self):
        return None

    def get_competition_metrics(self, competition):

        num_to_display = 5

        metrics_names = []
        metrics_names.append(('hanging_points', "Hanging Points"))
        metrics_names.append(('pyramid_goals', "Pyramid Goals"))
        metrics_names.append(('high_goals', "High Goals"))
        metrics_names.append(('mid_goals', "Mid Goals"))
        metrics_names.append(('low_goals', "Low Goals"))

        output = []

        for metric, full_name in metrics_names:
            result = ScoreResult.objects.filter(competition=competition).values('team__teamNumber').annotate(the_result=Avg(metric)).order_by('-the_result')[0:num_to_display]

            this_result = [(x['team__teamNumber'], "%.2f" % x['the_result']) for x in result]
            print this_result
            output.append((full_name, this_result))

        return output


class AddTeamCommentsView2013(BaseAddTeamCommentsView):

    def __init__(self):
        BaseAddTeamCommentsView.__init__(self, Team, TeamComments, 'Scouting2013:view_team')


class AddTeamPictureView2013(BaseAddTeamPictureView):

    def __init__(self):
        BaseAddTeamPictureView.__init__(self, Team, TeamPictures, 'Scouting2013/static', 'Scouting2013/robot_pics', 'Scouting2013:view_team')


class AllTeamsViews2013(BaseAllTeamsViews):

    def __init__(self):
        BaseAllTeamsViews.__init__(self, TeamCompetesIn, 'Scouting2013/all_teams.html')

    def get_metrics_for_team(self, team):
        return get_team_metrics(team)


class SingleTeamView2013(BaseSingleTeamView):

    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, 'Scouting2013/view_team.html')

    def get_metrics(self, team):
        return get_team_metrics(team)


class AllMatchesView2013(BaseAllMatchesView):

    def __init__(self):
        BaseAllMatchesView.__init__(self, Match, OfficialMatch, 'Scouting2013/all_matches.html')


class SingleMatchView2013(BaseSingleMatchView):

    def __init__(self):
        BaseSingleMatchView.__init__(self, Match, 'Scouting2013/view_match.html')

    def get_metrics(self, sr):
        output = []
        output.append(('teamNumber', sr.team.teamNumber))
        sr_fields = ScoreResult.get_fields()
        for key in sr_fields:
            sr_field = sr_fields[key]
            output.append((sr_field.display_name, getattr(sr, key)))

        return output


class GenGraphView2013(BaseGenGraphView):

    def __init__(self):
        BaseGenGraphView.__init__(self, Team)


class OfficialMatchView2013(BaseMatchPredictionView):

    def __init__(self):
        BaseMatchPredictionView.__init__(self, OfficialMatch, 'Scouting2013/view_official_match.html')

    def get_score_results(self, official_match):

        results = official_match.officialmatchscoreresult_set.all()
        blue_results = results[0]
        red_results = results[1]

        output = {}
        output['red_results'] = red_results
        output['blue_results'] = blue_results

        return output
