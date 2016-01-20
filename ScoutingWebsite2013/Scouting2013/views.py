from django.shortcuts import render
from django.db.models import Avg, Sum
from Scouting2013.models import Team, Match

# Create your views here.


def __get_team_metrics(team):
    metrics = team.scoreresult_set.aggregate(Avg('auton_score'), 
                                          Avg('pyramid_goals'),
                                          Avg('high_goals'),
                                          Avg('mid_goals'),
                                          Avg('low_goals'),
                                          Avg('missed_shots'),
                                          Avg('hanging_points'),
                                          Avg('fouls'),
                                          Avg('technical_fouls'),
                                          Sum('invalid_hangs'),
                                          Sum('yellow_card'),
                                          Sum('red_card'),
                                          Sum('broke_badly'),
                                          )
    
    #Format all of the numbers.  If we haven't scouted the team, None will be returned.  Turn that into NA
    for key in metrics:
        if metrics[key] == None:
            metrics[key] = "NA"
        elif "__avg" in key:
            metrics[key] = "{:10.2f}".format(metrics[key])
            
    return metrics


def index(request):

    return render(request, 'Scouting2013/index.html')


def all_teams(request):

    all_teams = Team.objects.all()
    
    teams_with_avg = []
    
    for team in all_teams:
        
        metrics = __get_team_metrics(team)
                
        team_with_avg = {"id": team.id, 
                         "teamNumber": team.teamNumber,
                         "matches_scouted": team.scoreresult_set.count(),
                         "avgerages": metrics,
                        }
        teams_with_avg.append(team_with_avg)

    context = {"teams": teams_with_avg}

    return render(request, 'Scouting2013/all_teams.html', context)


def view_team(request, team_id):

    this_team = Team.objects.get(id=team_id)
    
    metrics = __get_team_metrics(this_team)
    match_list = []
    
    for sr in this_team.scoreresult_set.all():
        match_list.append(sr.match)
    

    context = {"id": this_team.id, 
               "teamNumber": this_team.teamNumber,
               "metrics": metrics,
               "match_list": match_list,
              }

    return render(request, 'Scouting2013/single_team.html', context)


def all_matches(request):
    
    all_matches = Match.objects.all()
    
    context = {"matches": all_matches}

    return render(request, 'Scouting2013/all_matches.html', context)


def view_match(request, match_id):

    this_match = Match.objects.get(id=match_id)
    results = this_match.scoreresult_set.all()
    
    context = {"id": this_match.id, 
               "matchNumber": this_match.matchNumber,
               "results": results,
              }

    return render(request, 'Scouting2013/single_match.html', context)
