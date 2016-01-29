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

def showForm(request):

    return render(request, 'Scouting2016/inputForm.html')

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
    print request.POST
    team = Team.objects.get(teamNumber=request.POST["team_number"])
    if len(Match.objects.filter(matchNumber=request.POST["match_number"])) == 0:
        print "Creating match!"
        match = Match.objects.create(matchNumber=request.POST["match_number"])
    else :
        match = Match.objects.get(matchNumber=request.POST["match_number"])
        
    score_result = ScoreResult.objects.create(match=match, 
                                              team=team,
                                              team_number=team.teamNumber,
                                              match_number=match.matchNumber,
                                              auto_score_low = request.POST["auto_score_low"],
                                              auto_score_high = request.POST["auto_score_high"],
                                              cheval_de_frise = request.POST["cheval_de_frise"],
                                              ramparts = request.POST["ramparts"],
                                              sally_port = request.POST["sally_port"],
                                              low_bar = request.POST["low_bar"],
                                              rock_wall = request.POST["rock_wall"],
                                              draw_bridge = request.POST["draw_bridge"],
                                              moat = request.POST["moat"],
                                              rough_terrain = request.POST["rough_terrain"],  
                                              score_tech_foul = request.POST["score_tech_foul"],
                                              high_score_fail = request.POST["high_score_fail"],
                                              high_score_successful = request.POST["high_score_successful"],
                                              low_score_successful = request.POST["low_score_successful"],
                                              low_score_fail = request.POST["low_score_fail"],
                                              notes_text_area = request.POST["notes_text_area"],)
    
        
        
    print "Adding SR: %s, %s" % (team, match)   
    return render(request, 'Scouting2016/index.html')