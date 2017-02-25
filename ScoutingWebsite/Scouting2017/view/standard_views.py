from BaseScouting.views.base_views import BaseHomepageView, BaseTeamListView,\
    BaseSingleMatchView, BaseMatchListView, BaseSingleTeamView, BaseMatchEntryView, BaseAddTeamPictureView,\
    BaseMatchPredictionView
from Scouting2017.model.reusable_models import Competition, TeamCompetesIn, Match, OfficialMatch, Team, TeamPictures, TeamComments,\
    Scout
from Scouting2017.model.models2017 import ScoreResult, get_team_metrics
from django.db.models.aggregates import Avg, Sum
from django.db.models.expressions import Case, When
from django.db.models import Q, F
import math
from django.http.response import HttpResponseRedirect, HttpResponse,\
    HttpResponseNotFound
from django.core.urlresolvers import reverse
import math,json
from django.views.generic.base import TemplateView
import operator
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def validate_alliance_score(alliance_color, team1, team2, team3, official_sr):
    team1sr = None
    team2sr = None
    team3sr = None
    
    # TODO: there has to be a better way... but I'd rather not touch the DB
    for sr in team1.scoreresult_set.all():
        if sr.match.matchNumber == official_sr.official_match.matchNumber:
            team1sr = sr
            break
    
    for sr in team2.scoreresult_set.all():
        if sr.match.matchNumber == official_sr.official_match.matchNumber:
            team2sr = sr
            break
    
    for sr in team3.scoreresult_set.all():
        if sr.match.matchNumber == official_sr.official_match.matchNumber:
            team3sr = sr
            break
        
    warning_messages = []
    error_messages = []

    team_srs = [team1sr, team2sr, team3sr]
    
    auto_fuel_low_sum = 0
    auto_fuel_high_sum = 0
    tele_fuel_low_sum = 0
    tele_fuel_high_sum = 0
    
    auto_gear_sum = 0
    tele_gear_sum = 0
    
    climb_sum = 0
    basline_sum = 0
    
    for sr in team_srs:
        auto_fuel_low_sum += sr.auto_fuel_low_score
        auto_fuel_high_sum += sr.auto_fuel_high_score
        tele_fuel_low_sum += sr.tele_fuel_low_score
        tele_fuel_high_sum += sr.tele_fuel_high_score
        
        auto_gear_sum += sr.tele_gears
        tele_gear_sum += sr.tele_gears
        
        climb_sum += 1 if sr.rope else 0
        basline_sum += 1 if sr.auto_baseline else 0
        
    ######################
    # Fuel
    ######################
    if official_sr.autoFuelLow != auto_fuel_low_sum:
        warning_messages.append((alliance_color + "Auto Low Fuel", official_sr.autoFuelLow, auto_fuel_low_sum))
        
    if official_sr.autoFuelHigh != auto_fuel_high_sum:
        warning_messages.append((alliance_color + "Auto High Fuel", official_sr.autoFuelHigh, auto_fuel_high_sum))
        
    if official_sr.teleopFuelLow != tele_fuel_low_sum:
        warning_messages.append((alliance_color + "Tele Low Fuel", official_sr.teleopFuelLow, tele_fuel_low_sum))
        
    if official_sr.teleopFuelHigh != tele_fuel_high_sum:
        warning_messages.append((alliance_color + "Tele High Fuel", official_sr.teleopFuelHigh, tele_fuel_high_sum))
        
        
    #######################
    # Gears
    #######################    
    auto_rotors = 0
    if auto_gear_sum >= 1:
        auto_rotors += 1
    if auto_gear_sum >= 3:
        auto_rotors += 1
        
    tele_rotors = 0
    if tele_gear_sum >= 1:
        tele_rotors += 1
    if tele_gear_sum >= 3:
        tele_rotors += 1
    if tele_gear_sum >= 7:
        tele_rotors += 1
    if tele_gear_sum >= 13:
        tele_rotors += 1
        
    if official_sr.rotor1Auto == 1 and (auto_rotors >= 1) :
        error_messages.append((alliance_color + "Auto Rotors", 1, auto_rotors))
       
    if official_sr.rotor2Auto == 1 and (auto_rotors >= 2) :
        error_messages.append((alliance_color + "Auto Rotors", 2, auto_rotors))
        
    if len(error_messages) != 0:
        print error_messages
        
    
    #######################
    # Other
    #######################   
    official_rope_sum = 0
    if official_sr.touchpadNear:
        official_rope_sum += 1
    if official_sr.touchpadMiddle:
        official_rope_sum += 1
    if official_sr.touchpadFar:
        official_rope_sum += 1
        
    official_baseline_sum = 0
    if official_sr.robot1Auto:
        official_baseline_sum += 1
    if official_sr.robot2Auto:
        official_baseline_sum += 1
    if official_sr.robot3Auto:
        official_baseline_sum += 1
        
    if official_rope_sum != climb_sum:
        error_messages.append((alliance_color + "Climbing", official_rope_sum, climb_sum))
        
    if official_baseline_sum != basline_sum:
        error_messages.append((alliance_color + "Baseline", official_baseline_sum, basline_sum))
        
    if len(error_messages) != 0:
        print error_messages
        
    print warning_messages
    print error_messages

    return warning_messages, error_messages
        
        
#     if (auto_fuel_low_sum / 3.0 + tele_fuel_low_sum) !=  official_sr.
        
#     print auto_fuel_low_sum, auto_fuel_high_sum, tele_fuel_low_sum, tele_fuel_high_sum


def calculate_match_scouting_validity(match, official_match, official_match_srs):
    
    error_level = 0
    warning_messages = []
    error_messages = []
    
    if len(match.scoreresult_set.all()) != 6:
        error_level = 2
    elif len(official_match_srs) == 2:
        red_official = official_match_srs[0]
        blue_official = official_match_srs[1]
        
        red_warning, red_error = validate_alliance_score("Red", match.red1, match.red2, match.red3, red_official)
        blue_warning, blue_error = validate_alliance_score("Blue", match.blue1, match.blue2, match.blue3, blue_official)
        
        warning_messages.extend(red_warning)
        warning_messages.extend(blue_warning)
        error_messages.extend(red_error)
        error_messages.extend(blue_error)
        
        if len(error_messages) != 0:
            error_level = 2
        elif len(warning_messages) != 0:
            error_level = 1
            
        
#         print match.red1
    else:
        error_level = 1
                
        
    
    return error_level, warning_messages, error_messages

class HomepageView2017(BaseHomepageView):
 
    def __init__(self):
        BaseHomepageView.__init__(self, Competition, 'BaseScouting/index.html')
 
    def get_our_metrics(self):
 
        return []
 
    def get_competition_metrics(self, competition):
 
        output = []
 
        return output

class TeamListView2017(BaseTeamListView):
    def __init__(self):
        BaseTeamListView.__init__(self, TeamCompetesIn, ScoreResult, 'Scouting2017/team_list.html')

    def get_metrics_for_team(self, team):
        return get_team_metrics(team)
    
    def get_context_data(self, **kwargs):
        
        user = self.request.user
        
        context = BaseTeamListView.get_context_data(self, **kwargs)
        reg_code = kwargs['regional_code']
#         teams_at_competition = TeamCompetesIn.objects.filter(competition__code=reg_code)
        stats = get_statistics(reg_code, context['teams'])
        context['stats'] = stats[0]
        context['skills'] = stats[1]
        
        for team in context['teams']:
            team.bookmarkCount = team.bookmarks.count()
            team.dnpCount = team.do_not_picks.count()
            
            if user != None and user.is_authenticated():
                team.isBookmarked = team in user.scout.bookmarked_teams.all()
                team.isDoNotPick = team in user.scout.do_not_pick_teams.all()
#             team.isBookmarked = user.scou
        
        
        return context
        
class AddTeamPictureView2017(BaseAddTeamPictureView):

    def __init__(self):
        BaseAddTeamPictureView.__init__(self, Team, TeamPictures, 'Scouting2017/static', 'Scouting2017/robot_pics', 'Scouting2017:view_team')

        
class SingleMatchView2017(BaseSingleMatchView):

    def __init__(self):
        BaseSingleMatchView.__init__(self, Match, 'Scouting2017/match.html')
        
    def get_context_data(self, **kwargs):
        context = BaseSingleMatchView.get_context_data(self, **kwargs)
        
        match = context['match']
        
        print match.red1.scoreresult_set.filter(match=match)[0].team
         
        context['red'] = {}
        context['red']['sr1'] = match.red1.scoreresult_set.filter(match=match)[0]
        context['red']['sr2'] = match.red2.scoreresult_set.filter(match=match)[0]
        context['red']['sr3'] = match.red3.scoreresult_set.filter(match=match)[0]
         
        context['blue'] = {}
        context['blue']['sr1'] = match.blue1.scoreresult_set.filter(match=match)[0]
        context['blue']['sr2'] = match.blue2.scoreresult_set.filter(match=match)[0]
        context['blue']['sr3'] = match.blue3.scoreresult_set.filter(match=match)[0]
        
        return context

    def get_metrics(self, score_result):
        return []
    
    def get_match_validation(self, match):

        official_match = OfficialMatch.objects.get(matchNumber=match.matchNumber)
        official_sr_search = official_match.officialmatchscoreresult_set.all()
        if len(official_sr_search) == 2:
            _, warnings, errors = calculate_match_scouting_validity(match, official_match, official_sr_search)

            return True, warnings, errors

        return False, [], []

class MatchListView2017(BaseMatchListView):
    def __init__(self):
        BaseMatchListView.__init__(self, Match)
    
    def append_scouted_info(self, match, regional_code):
        
        output = match
        
        output.match_error_level = 0
        output.match_error_warning_messages = []
        output.match_error_error_messages = []
        output.winning_alliance = "Unofficial"
        output.redScore = "Unknown"
        output.blueScore = "Unknown"
        
        
        official_match_search = OfficialMatch.objects.filter(competition__code=regional_code, matchNumber=match.matchNumber)
        if len(official_match_search) == 1:
            official_match = official_match_search[0]
            official_sr_search = official_match.officialmatchscoreresult_set.all()
            if len(official_sr_search) == 2:
                red_score = official_sr_search[0].totalPoints
                blue_score = official_sr_search[1].totalPoints
                
                output.redScore = red_score
                output.blueScore = blue_score
                
                if red_score > blue_score:
                    output.winning_alliance = "Red"
                elif blue_score > red_score:
                    output.winning_alliance = "Blue"
                else:
                    output.winning_alliance = "Tie"
                
            output.match_error_level, output.match_error_warning_messages, output.match_error_error_messages = calculate_match_scouting_validity(match, official_match, official_sr_search)

        return output

class SingleTeamView2017(BaseSingleTeamView):

    def __init__(self):
        BaseSingleTeamView.__init__(self, Team, TeamPictures, TeamComments, 'Scouting2017/team.html')

    def get_context_data(self, **kwargs):
        context = BaseSingleTeamView.get_context_data(self, **kwargs)
        
        if context['metrics']['tele_fuel_high_score__avg'] != "NA":
        
            context['metrics']['tele_fuel_high_misses__avg'] = float(context['metrics']['tele_fuel_high_shots__avg']) - float(context['metrics']['tele_fuel_high_score__avg'])
            context['metrics']['auto_fuel_high_misses__avg'] = float(context['metrics']['auto_fuel_high_shots__avg']) - float(context['metrics']['auto_fuel_high_score__avg'])
            context['metrics']['tele_fuel_low_misses__avg']  = float(context['metrics']['tele_fuel_low_shots__avg'])  - float(context['metrics']['tele_fuel_low_score__avg'])
            context['metrics']['auto_fuel_low_misses__avg']  = float(context['metrics']['auto_fuel_low_shots__avg'])  - float(context['metrics']['auto_fuel_low_score__avg'])
#             context['metrics']['fuel_shot_hi_missed_auto__avg'] = float(context['metrics']['fuel_shot_hi_auto__avg']) - float(context['metrics']['fuel_score_hi_auto__avg'])
#             context['metrics']['fuel_shot_low_missed__avg'] = float(context['metrics']['fuel_shot_low__avg']) - float(context['metrics']['fuel_score_low__avg'])
#             context['metrics']['fuel_shot_low_missed_auto__avg'] = float(context['metrics']['fuel_shot_low_auto__avg']) - float(context['metrics']['fuel_score_low_auto__avg'])
        else:
            context['metrics']['tele_fuel_high_misses__avg'] = "NA"
            context['metrics']['auto_fuel_high_misses__avg'] = "NA"
            context['metrics']['fuel_shot_low_missed__avg'] = "NA"
            context['metrics']['fuel_shot_low_missed_auto__avg'] = "NA"
        
        return context
        
    def get_metrics(self, team):
        return get_team_metrics(team)
    

def get_team_average_for_match_prediction(team, regional_code):
    
    output = team.scoreresult_set.filter(competition__code=regional_code).aggregate(
        auto_fuel_high=Avg("auto_fuel_high_score"),
        auto_fuel_low=Avg("auto_fuel_low_score"),
        auto_gears=Avg("tele_gears"),
        tele_fuel_high=Avg("tele_fuel_high_score"),
        tele_fuel_low=Avg("tele_fuel_low_score"),
        tele_gears=Avg("tele_gears"),
        baseline=Avg(Case(When(auto_baseline=True, then=1),When(auto_baseline=False, then=0))),
        rope=Avg(Case(When(rope=True, then=1),When(rope=False, then=0))),
        )
    
    output["team_number"] = team.teamNumber
    
    fuel_total = output['auto_fuel_high'] + \
                 output['auto_fuel_low'] / 3.0 + \
                 output['tele_fuel_high'] / 3.0 + \
                 output['tele_fuel_low'] / 9.0
    
    output["fuel_total"] = fuel_total
    output["total_score"] = fuel_total + \
                              output['auto_baseline'] * 5 + \
                              output['rope'] * 50
    
    return output
    
    
def get_alliance_average_for_match_prediction(team1, team2, team3, regional_code):
    
    team1_metrics = get_team_average_for_match_prediction(team1, regional_code)
    team2_metrics = get_team_average_for_match_prediction(team2, regional_code)
    team3_metrics = get_team_average_for_match_prediction(team3, regional_code)
    
    averages = {}
    
    for key in team1_metrics.keys():
        averages[key] = float(team1_metrics[key]) + float(team2_metrics[key]) + float(team3_metrics[key]) 
        
    
    output = {}
    output['team1'] = team1_metrics
    output['team2'] = team2_metrics
    output['team3'] = team3_metrics
    output['averages'] = averages
    output['total_score'] = averages["total_score"]
    output['kpa_bonus'] = "Yes" if averages["fuel_total"] >= 40 else "No"
    output['rotor_bonus'] = "Yes"
        
    return output
    
class MatchPredictionView2017(BaseMatchPredictionView):
    def __init__(self):
        BaseMatchPredictionView.__init__(self, Match, 'Scouting2017/match_prediction.html')
        
    def get_score_results(self, match, regional_code):
        
        output = {}
        
        output['red_prediction'] = get_alliance_average_for_match_prediction(match.red1, match.red2, match.red3, regional_code)
        output['blue_prediction'] = get_alliance_average_for_match_prediction(match.blue1, match.blue2, match.blue3, regional_code)

        return output
        
        
class PickListView2017(TemplateView):
    def __init__(self):
        self.template_name = 'Scouting2017/pick_list.html'

    def get_context_data(self, **kwargs):
        context = super(PickListView2017, self).get_context_data(**kwargs)

        all_teams = []
        for team_competes_in in TeamCompetesIn.objects.filter(competition__code=kwargs['regional_code']):
            all_teams.append(team_competes_in.team)
            
        all_teams = sorted(all_teams, key=operator.attrgetter('teamNumber'))
        
        context['original_overall_list'] = []
        context['original_fuel_list'] = []
        context['original_gear_list'] = []
        context['original_defense_list'] = []
        context['original_dnp_list'] = []
        context['all_teams'] = all_teams
        
        context['original_overall_list'].append(Team.objects.get(teamNumber=174))
        context['original_fuel_list'].append(Team.objects.get(teamNumber=1507))
        context['original_fuel_list'].append(Team.objects.get(teamNumber=1126))
        context['original_fuel_list'].append(Team.objects.get(teamNumber=340))
        context['original_gear_list'].append(Team.objects.get(teamNumber=174))
        context['original_gear_list'].append(Team.objects.get(teamNumber=191))
        context['original_gear_list'].append(Team.objects.get(teamNumber=1507))
        context['original_defense_list'].append(Team.objects.get(teamNumber=1405))
        context['original_dnp_list'].append(Team.objects.get(teamNumber=1450))
        
        return context


def update_bookmark(request, **kwargs):
    
    if request.user == None or not request.user.is_authenticated():
        return HttpResponseNotFound('<h1>Must be logged in!</h1>')  
    
    user = request.user
    team = Team.objects.get(teamNumber=request.POST['team_number'])
    bookmark_type = request.POST["bookmark_type"]
    
    if bookmark_type == "bookmark":
        is_bookmarked = team in user.scout.bookmarked_teams.all()
        
        if is_bookmarked:
            user.scout.bookmarked_teams.remove(team)
        else:
            user.scout.bookmarked_teams.add(team)
    elif bookmark_type == "do_not_pick":
        is_bookmarked = team in user.scout.do_not_pick_teams.all()
        
        if is_bookmarked:
            user.scout.do_not_pick_teams.remove(team)
        else:
            user.scout.do_not_pick_teams.add(team)
    else:
        print "unknown bookmark type %s" % bookmark_type
    
    response = {'is_bookmarked': not is_bookmarked}
    
    return HttpResponse(json.dumps(response), content_type='application/json')
    
'''
The get_statistics function() returns two lists of metrics.
The first thing it returns, stats, is a dictionary containing the values of overall averages for all score results, along with standard deviations for those same score results along the mean.
The function also returns a list called skills, which contains data for each team including their z-scores, calculated fuel scores for both hi, low, autonomous, teleop, and overall, and their accuracy in climbing the rope. 
'''
def get_statistics(regional_code, teams_at_competition, team=0):
    
    skills = []
       
    competition_srs = ScoreResult.objects.filter(competition__code=regional_code)
    competition_averages = competition_srs.aggregate(
                                                     Avg('auto_fuel_high_score'),
                                                     Avg('auto_fuel_low_score'),
                                                     Avg('tele_gears'),
                                                     Avg('tele_fuel_high_score'),
                                                     Avg('tele_fuel_low_score'),
                                                     rope__avg = Avg(Case(When(rope=True, then=1),When(rope=False, then=0))))
    rope_avg = competition_averages['rope__avg']
    gear_avg = competition_averages['tele_gears__avg']

    if competition_averages['auto_fuel_high_score__avg'] and competition_averages['tele_fuel_high_score__avg'] and competition_averages['auto_fuel_low_score__avg'] and competition_averages['tele_fuel_low_score__avg']:
        
        fuel_avg = competition_averages['auto_fuel_high_score__avg'] + (competition_averages['tele_fuel_high_score__avg'] / 3 ) + (competition_averages['auto_fuel_low_score__avg'] / 3) + (competition_averages['tele_fuel_low_score__avg'] / 9)
    else:
        fuel_avg = 0
   # This part of the function (above) obtains overall averages for all score results
    num_srs = 0 
    gear_v2 = 0
    fuel_v2 = 0
    rope_v2 = 0
    num_srs = 0 
    
    for sr in competition_srs: 
        if sr.rope==True:
            sr_rope =1-rope_avg
        else:
            sr_rope = 0-rope_avg     
        sr_gear = sr.tele_gears - gear_avg
        sr_fuel = ((sr.auto_fuel_high_score)+(sr.tele_fuel_high_score / 3) + (sr.auto_fuel_low_score / 3) + (sr.tele_fuel_low_score / 9)) - fuel_avg
        gear_v2 += sr_gear * sr_gear
        fuel_v2 += sr_fuel * sr_fuel
        rope_v2 += sr_rope * sr_rope 
        num_srs += 1  
        
    if num_srs == 0:
        gear_stdev = 0 
        fuel_stdev = 0
        rope_stdev = 0
    else:
        gear_stdev = math.sqrt(gear_v2/num_srs) 
        fuel_stdev = math.sqrt(fuel_v2/num_srs)
        rope_stdev = math.sqrt(rope_v2/num_srs)
        
    # This part of the function (above) obtains overall standard deviations for all score results
    teams = team if bool(team) else teams_at_competition
    for team in teams:
        teams_srs = team.scoreresult_set.filter(competition__code=regional_code) 
        team_avgs = teams_srs.aggregate(Avg('tele_gears'),
                                        Avg('tele_fuel_high_score'),
                                        Avg('auto_fuel_high_score'),
                                        Avg('tele_fuel_low_score'),
                                        Avg('auto_fuel_low_score'),
                                        team_rope__avg = Avg(Case(When(rope=True, then=1),When(rope=False, then=0))))
                                      
        team_rope_avg = team_avgs['team_rope__avg']
        team.skills = {}
        team.skills['fuel_z'] = 'NA'
        team.skills['gear_z'] = 'NA'
        team.skills['rope_z'] = 'NA'
        team.skills['rope_pct'] = 'NA'
        if len(teams_srs)!= 0:
            team.skills['fuel_score'] = ((team_avgs['auto_fuel_high_score__avg']) + (team_avgs['tele_fuel_high_score__avg'] / 3) + (team_avgs['auto_fuel_low_score__avg'] / 3) + (team_avgs['tele_fuel_low_score__avg']/ 9))
            team.skills['gear_z'] = (team_avgs['tele_gears__avg'] - gear_avg ) / gear_stdev 
            team.skills['fuel_z'] = (((team_avgs['auto_fuel_high_score__avg']) + (team_avgs['tele_fuel_high_score__avg'] / 3) + (team_avgs['auto_fuel_low_score__avg'] / 3) + (team_avgs['tele_fuel_low_score__avg']/ 9)) - fuel_avg) / fuel_stdev
            team.skills['rope_z'] = (team_avgs['team_rope__avg'] - rope_avg) / rope_stdev
            team.skills['rope_pct'] = team_avgs['team_rope__avg'] * 100
            
        skills.append({'team': team.teamNumber, 'skills':team.skills})

    stats = {'gear_avg': gear_avg, 'rope_avg': rope_avg, 'fuel_avg': fuel_avg, 'fuel_hi_avg': team_avgs['tele_fuel_high_score__avg'], 'fuel_low_avg': team_avgs['tele_fuel_low_score__avg'],
             'fuel_hi_auto_avg': team_avgs['auto_fuel_high_score__avg'], 'fuel_low_auto_avg': team_avgs['auto_fuel_low_score__avg'], 'gear_stdev': gear_stdev, 'rope_stdev': rope_stdev, 'fuel_stdev': fuel_stdev}

    
    return (stats,json.dumps(skills))   
