
from Scouting2011.model.reusable_models import Team, Match, OfficialMatch, TeamPictures, TeamComments, TeamCompetesIn
from Scouting2011.model.models2011 import ScoreResult, get_team_metrics
from BaseScouting.views.base_views import BaseAddTeamCommentsView, \
    BaseAddTeamPictureView, BaseAllTeamsViews, BaseSingleTeamView, \
    BaseAllMatchesView, BaseSingleMatchView, BaseOfficialMatchView, \
    BaseGenGraphView


class AddTeamCommentsView2011(BaseAddTeamCommentsView):

    def __init__(self):
        BaseAddTeamCommentsView.__init__(self, Team, TeamComments, 'Scouting2011:view_team')


class AddTeamPictureView2011(BaseAddTeamPictureView):

    def __init__(self):
        BaseAddTeamPictureView.__init__(self, Team, TeamPictures, 'Scouting2011/static', 'Scouting2011/robot_pics', 'Scouting2011:view_team')


class AllTeamsViews2011(BaseAllTeamsViews):

    def __init__(self):
        BaseAllTeamsViews.__init__(self, TeamCompetesIn, 'Scouting2011/all_teams.html')

    def get_metrics_for_team(self, team):
        all_fields = ScoreResult.get_fields()
        del all_fields['was_offensive']
        del all_fields['was_scouted']
        del all_fields['broke_badly']

        return get_team_metrics(team, all_fields)


class SingleTeamView2011(BaseSingleTeamView):

    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, 'Scouting2011/view_team.html')

    def get_metrics(self, team):
        all_fields = ScoreResult.get_fields()
        del all_fields['was_offensive']

        return get_team_metrics(team, all_fields)


class AllMatchesView2011(BaseAllMatchesView):

    def __init__(self):
        BaseAllMatchesView.__init__(self, Match, OfficialMatch, 'Scouting2011/all_matches.html')


class SingleMatchView2011(BaseSingleMatchView):

    def __init__(self):
        BaseSingleMatchView.__init__(self, Match, 'Scouting2011/view_match.html')

    def get_metrics(self, sr):
        output = []
        output.append(('teamNumber', sr.team.teamNumber))
        sr_fields = ScoreResult.get_fields()
        for key in sr_fields:
            sr_field = sr_fields[key]
            output.append((sr_field.display_name, getattr(sr, key)))

        return output


class GenGraphView2011(BaseGenGraphView):

    def __init__(self):
        BaseGenGraphView.__init__(self, Team)


class OfficialMatchView2011(BaseOfficialMatchView):

    def __init__(self):
        BaseOfficialMatchView.__init__(self, OfficialMatch, 'Scouting2011/view_official_match.html')

    def get_score_results(self, official_match):

        results = official_match.officialmatchscoreresult_set.all()
        blue_results = results[0]
        red_results = results[1]

        output = {}
        output['red_results'] = red_results
        output['blue_results'] = blue_results

        return output
