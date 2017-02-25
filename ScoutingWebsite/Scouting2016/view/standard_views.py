import operator
from Scouting2016.model.reusable_models import Team, Match, OfficialMatch, TeamPictures, TeamComments, TeamCompetesIn, Competition
from Scouting2016.model.models2016 import get_team_metrics, get_defense_stats, \
    get_advanced_team_metrics, ScoreResult
from BaseScouting.views.base_views import *
from django.db.models.aggregates import Avg, Sum


class HomepageView2016(BaseHomepageView):

    def __init__(self):
        BaseHomepageView.__init__(self, Competition)

    def get_our_metrics(self):

        team_search = Team.objects.filter(teamNumber=174)

        if len(team_search) == 0:
            return None

        all_fields = ScoreResult.get_fields()
        metrics_of_interest = {}
        metrics_of_interest['low_score_successful'] = all_fields['low_score_successful']

        return get_advanced_team_metrics(team_search[0], metrics_of_interest)

    def get_competition_metrics(self, competition):

        num_to_display = 5

        metrics_names = []
        metrics_names.append(('high_score_successful', "High Goals"))
        metrics_names.append(('auto_score_high', "Auton High Goals"))
        metrics_names.append(('low_score_successful', "Low Goals"))
        metrics_names.append(('auto_score_low', "Auton Low Goals"))

        output = []

        for metric, full_name in metrics_names:
            result = ScoreResult.objects.filter(competition=competition).values('team__teamNumber').annotate(the_result=Avg(metric)).order_by('-the_result')[0:num_to_display]

            this_result = [(x['team__teamNumber'], "%.2f" % x['the_result']) for x in result]
            print this_result
            output.append((full_name, this_result))

        return output


class AddTeamCommentsView2016(BaseAddTeamCommentsView):

    def __init__(self):
        BaseAddTeamCommentsView.__init__(self, Team, TeamComments, 'Scouting2016:view_team')


class AddTeamPictureView2016(BaseAddTeamPictureView):

    def __init__(self):
        BaseAddTeamPictureView.__init__(self, Team, TeamPictures, 'Scouting2016/static', 'Scouting2016/robot_pics', 'Scouting2016:view_team')


class TeamListView2016(BaseTeamListView):

    def __init__(self):
        BaseTeamListView.__init__(self, TeamCompetesIn, ScoreResult)
        
    def get_metrics_for_team(self, team):
        return get_team_metrics(team)


class SingleTeamView2016(BaseSingleTeamView):

    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, 'Scouting2016/view_team.html')

    def get_metrics(self, team):
        return get_team_metrics(team)


class MatchListView2016(BaseMatchListView):

    def __init__(self):
        BaseMatchListView.__init__(self, Match, OfficialMatch)


class SingleMatchView2016(BaseSingleMatchView):

    def __init__(self):
        BaseSingleMatchView.__init__(self, Match, 'Scouting2016/match.html')

    def get_metrics(self, score_result):
        return []


class GenGraphView2016(BaseGenGraphView):

    def __init__(self):
        BaseGenGraphView.__init__(self, Team)


class OfficialMatchView2016(BaseMatchPredictionView):

    def __init__(self):
        BaseMatchPredictionView.__init__(self, OfficialMatch, 'Scouting2016/official_match.html')

    def __get_sorted_defense_stats(self, official_score_result):
        results = {}

        get_defense_stats(official_score_result.team1, results)
        get_defense_stats(official_score_result.team2, results)
        get_defense_stats(official_score_result.team3, results)

        for category in results:
            results[category] = sorted(results[category].items(), key=operator.itemgetter(1), reverse=True)

        return sorted(results.items())

    def get_score_results(self, official_match):

        results = official_match.officialmatchscoreresult_set.all()
        blue_results = results[0]
        red_results = results[1]

        output = {}
        output['red_results'] = red_results
        output['blue_results'] = blue_results

        output['red_defenses'] = self.__get_sorted_defense_stats(red_results)
        output['blue_defenses'] = self.__get_sorted_defense_stats(blue_results)

        return output
