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
                                             Sum("portcullis"),
                                             
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


def __get_score_result_fields():
    
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
    output['scale_challenge'] = 'partial'    
    output['slow_fast_bridge'] = 'slow'
    output['slow_fast_cheval'] = 'fast'
    output['slow_fast_low_bar'] = 'slow'
    output['slow_fast_moat'] = 'slow'
    output['slow_fast_portcullis'] = 'slow'
    output['slow_fast_ramparts'] = 'no_move'
    output['slow_fast_rock_wall'] = 'no_move'
    output['slow_fast_rough'] = 'slow'
    output['slow_fast_sally'] = 'slow'
    
    return output

    

def index(request):
    
    return render(request, 'Scouting2016/index.html')

def info_for_form_edit(request):
    
    return render(request, 'Scouting2016/info_for_form_edit.html')

def showForm(request):
    score_result = __get_score_result_fields()
    
    context = {}
    context['team_number'] = 0
    context['match_number'] = 0
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
    
    context = {}
    context['team_number'] = this_team.teamNumber
    context['metrics'] = metrics
    context['score_result_list'] = score_result_list
    
    return render(request, 'Scouting2016/TeamPage.html', context)

def match_display(request, match_number):
    context = {}
    context['match_display'] = match_number
    print context
    return render(request, 'Scouting2016/MatchPage.html', context)

def edit_form(request):
    
    match = Match.objects.get(matchNumber=request.GET["match_number"])
    team = Team.objects.get(teamNumber=request.GET["team_number"])
    
    score_results = ScoreResult.objects.get(match_id=match.id, team_id=team.id)
    
    context = {}
    context['team_number'] = request.GET["team_number"]
    context['match_number'] = request.GET["match_number"]
    context['sr'] = score_results
    
    return render(request, 'Scouting2016/inputForm.html', context)


#Change^^^^^
def all_teams(request):
    
    the_teams = Team.objects.all()
    
    teams_with_avg = []
    
    for team in the_teams:
        
        metrics = __get_team_metrics(team)
                
        team_with_avg = {}
        team_with_avg["id"] = team.id
        team_with_avg["teamNumber"] = team.teamNumber
        team_with_avg["matches_scouted"] = team.scoreresult_set.count()
        team_with_avg["avgerages"] = metrics
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
            print key, value
#             setattr(score_result, key, value)
#         score_result.save()
#         print score_result
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
    
    score_result_fields_with_default= __get_score_result_fields()
    
    for field_name in score_result_fields_with_default:
        if field_name not in request.POST:
            kargs[field_name] = score_result_fields_with_default[field_name]
        else:
            kargs[field_name] = request.POST[field_name]
          
    return kargs
    