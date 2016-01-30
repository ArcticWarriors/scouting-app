from django.shortcuts import render
from django.template.context_processors import request
from Scouting2016.models import Team, Match, ScoreResult
from django.db.models import Avg, Sum

# Create your views here.
def __get_team_metrics(team):                                                                              
    metrics = team.scoreresult_set.aggregate(Avg("auto_score_low"),
                                          Avg("auto_score_high"),
                                           Sum("cheval_de_frise"),
                                           Sum("ramparts"),
                                           Sum("sally_port"),
                                           Sum("low_bar"),
                                           Sum("rock_wall"),
                                           Sum("draw_bridge"),                                          
                                           Sum("moat"),
                                           Sum("rough_terrain"),
                                           Sum("score_tech_foul"),
                                           Avg("high_score_fail"),
                                           Avg("high_score_successful"),
                                           Avg("low_score_fail"),
                                           Avg("low_score_successful"),
    
                                          
                                          
                                          )
    
    #Format all of the numbers.  If we haven't scouted the team, None will be returned.  Turn that into NA
    for key in metrics:
        if metrics[key] == None:
            metrics[key] = "NA"
        elif "__avg" in key:
            metrics[key] = "{:10.2f}".format(metrics[key])
            
    return metrics

    

def index(request):
    
    return render(request, 'Scouting2016/index.html')

def info_for_form_edit(request):
    
    return render(request, 'Scouting2016/info_for_form_edit.html')

def showForm(request):
    score_result = {}
    score_result['auto_score_high'] = 0
    score_result['auto_score_low'] = 0
    score_result['cheval_de_frise'] = 0
    score_result['draw_bridge'] = 0
    score_result['high_score_fail'] = 0
    score_result['high_score_successful'] = '0'
    score_result['low_bar'] = 0
    score_result['low_score_fail'] = 0
    score_result['low_score_successful'] = 0
    score_result['moat'] = 0
    score_result['notes_text_area'] = 0
    score_result['ramparts'] = 0
    score_result['rock_wall'] = 0
    score_result['rough_terrain'] = 0
    score_result['score_tech_foul'] = 0
    
    score_result['sally_port'] = 0
    score_result['auto_defense'] = 'auto_cross_ramparts'
    score_result['auto_spy'] = 'yes'
    score_result['portcullis'] = 5
    score_result['scale_challenge'] = 'scale_partial'    
    score_result['slow_fast_bridge'] = 'slow'
    score_result['slow_fast_cheval'] = 'fast'
    score_result['slow_fast_low_bar'] = 'slow'
    score_result['slow_fast_moat'] = 'slow'
    score_result['slow_fast_portcullis'] = 'slow'
    score_result['slow_fast_ramparts'] = 'no_move'
    score_result['slow_fast_rock_wall'] = 'no_move'
    score_result['slow_fast_rough'] = 'slow'
    score_result['slow_fast_sally'] = 'slow'
    
    context = {}
    context['team_number'] = 2000
    context['match_number'] = 1
    context["sr"] = score_result

    
    return render(request, 'Scouting2016/inputForm.html', context)

def robot_display(request):
    return render(request, 'Scouting2016/RobotDisplay.html')

def view_team(request, team_number):
    this_team = Team.objects.get(teamNumber=team_number)
    
    metrics = __get_team_metrics(this_team)
    score_result_list = []
    
    for sr in this_team.scoreresult_set.all():
        score_result_list.append(sr)
    

    context = { 
               "team_number": this_team.teamNumber,
               "metrics": metrics,
               "score_result_list": score_result_list,
              }
    
    context['team_number'] = team_number
    return render(request, 'Scouting2016/TeamPage.html', context)

def match_display(request, match_number):
    context = {}
    context['match_display'] = match_number
    print context
    return render(request, 'Scouting2016/MatchPage.html', context)

def edit_form(request):
    
    match = Match.objects.get(matchNumber=request.POST["match_number"])
    team = Team.objects.get(teamNumber=request.POST["team_number"])
    
    score_results = ScoreResult.objects.get(match_id=match.id, team_id=team.id)
    
    context = {}
    context['team_number'] = request.POST["team_number"]
    context['match_number'] = request.POST["match_number"]
    context['sr'] = score_results
    
    return render(request, 'Scouting2016/inputForm.html', context)


#Change^^^^^
def all_teams(request):
    
    the_teams = Team.objects.all()
    
    teams_with_avg = []
    
    for team in the_teams:
        
        metrics = __get_team_metrics(team)
                
        team_with_avg = {"id": team.id, 
                         "teamNumber": team.teamNumber,
                         "matches_scouted": team.scoreresult_set.count(),
                         "avgerages": metrics,
                        }
        teams_with_avg.append(team_with_avg)

    context = {"teams": teams_with_avg}
    
    return render(request, 'Scouting2016/AllTeams.html', context)

def all_matches(request):
    return render(request, 'Scouting2016/AllMatches.html')

def submitForm(request):
    team = Team.objects.get(teamNumber=request.POST["team_number"])
    if len(Match.objects.filter(matchNumber=request.POST["match_number"])) == 0:
        print "Creating match!"
        match = Match.objects.create(matchNumber=request.POST["match_number"])
    else :
        match = Match.objects.get(matchNumber=request.POST["match_number"])
        
    available_srs = ScoreResult.objects.filter(match=match,  team=team)
    
    kargs = __get_create_kargs(request)

    if len(available_srs) == 1:
        score_result = available_srs[0]
        
        for key, value in kargs.iteritems():
            setattr(score_result, key, value)
        score_result.save()
        print score_result
#         score_result.update(kargs)
    else:
        print "Creating, but not really"
        pass
        #__create_score_result(match, team, request)
        
#     kargs = __get_create_kargs(request)
#     score_result = ScoreResult.objects.create(match=match, 
#                                       team=team,
#                                       **kargs)
    
    
    print "Exists? %s" % available_srs

    print "Adding SR: %s, %s" % (team, match)   
    return render(request, 'Scouting2016/index.html')


def __get_create_kargs(request):
    
    kargs = {}
    
    kargs['auto_score_low'] = request.POST["auto_score_low"]
    kargs['auto_score_high'] = request.POST["auto_score_high"]
    kargs['cheval_de_frise'] = request.POST["cheval_de_frise"]
    kargs['ramparts'] = request.POST["ramparts"]
    kargs['sally_port'] = request.POST["sally_port"]
    kargs['low_bar'] = request.POST["low_bar"]
    kargs['rock_wall'] = request.POST["rock_wall"]
    kargs['draw_bridge'] = request.POST["draw_bridge"]
    kargs['moat'] = request.POST["moat"]
    kargs['rough_terrain'] = request.POST["rough_terrain"]  
    kargs['score_tech_foul'] = request.POST["score_tech_foul"]
    kargs['high_score_fail'] = request.POST["high_score_fail"]
    kargs['high_score_successful'] = request.POST["high_score_successful"]
    kargs['low_score_successful'] = request.POST["low_score_successful"]
    kargs['low_score_fail'] = request.POST["low_score_fail"]
    kargs['notes_text_area'] = request.POST["notes_text_area"]

    kargs['auto_spy'] = request.POST["auto_spy"]
    kargs['portcullis'] = request.POST["portcullis"]
    kargs['auto_defense'] = request.POST["auto_defense"]
    kargs['scale_challenge'] = request.POST["scale_challenge"]
    kargs['slow_fast_low_bar'] = request.POST["slow_fast_low_bar"]
    kargs['slow_fast_moat'] = request.POST["slow_fast_moat"]
    kargs['slow_fast_rock_wall'] = request.POST["slow_fast_rock_wall"]
    kargs['slow_fast_rough'] = request.POST["slow_fast_rough"]
    kargs['slow_fast_ramparts'] = request.POST["slow_fast_ramparts"]
    kargs['slow_fast_portcullis'] = request.POST["slow_fast_portcullis"]
    kargs['slow_fast_sally'] = request.POST["slow_fast_sally"]
    kargs['slow_fast_bridge'] = request.POST["slow_fast_bridge"]
    kargs['slow_fast_cheval'] = request.POST["slow_fast_cheval"]
          
    return kargs
    