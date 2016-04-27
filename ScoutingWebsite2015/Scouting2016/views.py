import operator
from Scouting2016.model.reusable_models import Team, Match, OfficialMatch, TeamPictures, TeamComments, TeamCompetesIn
from Scouting2016.model.models2016 import get_team_metrics, get_defense_stats
from BaseScouting.views.base_views import BaseAddTeamCommentsView, \
    BaseAddTeamPictureView, BaseAllTeamsViews, BaseSingleTeamView, \
    BaseAllMatchesView, BaseSingleMatchView, BaseOfficialMatchView,\
    BaseGenGraphView


class AddTeamCommentsView2016(BaseAddTeamCommentsView):

    def __init__(self):
        BaseAddTeamCommentsView.__init__(self, Team, TeamComments, 'Scouting2016:view_team')


class AddTeamPictureView2016(BaseAddTeamPictureView):

    def __init__(self):
        BaseAddTeamPictureView.__init__(self, Team, TeamPictures, 'Scouting2016/static', 'Scouting2016/robot_pics', 'Scouting2016:view_team')


class AllTeamsViews2016(BaseAllTeamsViews):

    def __init__(self):
        BaseAllTeamsViews.__init__(self, TeamCompetesIn, 'Scouting2016/all_teams.html')

    def get_metrics_for_team(self, team):
        return get_team_metrics(team)


class SingleTeamView2016(BaseSingleTeamView):

    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, 'Scouting2016/view_team.html')

    def get_metrics(self, team):
        return get_team_metrics(team)


class AllMatchesView2016(BaseAllMatchesView):

    def __init__(self):
        BaseAllMatchesView.__init__(self, Match, OfficialMatch, 'Scouting2016/all_matches.html')


class SingleMatchView2016(BaseSingleMatchView):

    def __init__(self):
        BaseSingleMatchView.__init__(self, Match, 'Scouting2016/view_match.html')


class GenGraphView2016(BaseGenGraphView):

    def __init__(self):
        BaseGenGraphView.__init__(self, Team)


class OfficialMatchView2016(BaseOfficialMatchView):

    def __init__(self):
        BaseOfficialMatchView.__init__(self, OfficialMatch, 'Scouting2016/view_official_match.html')

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
