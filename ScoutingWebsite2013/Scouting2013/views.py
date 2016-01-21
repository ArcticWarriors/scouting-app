from django.shortcuts import render
from django.db.models import Avg, Sum
from django.http.response import HttpResponse
from Scouting2013.models import Team, Match

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.font_manager import FontProperties

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


def view_graph(request, team_ids=[], fields=[]):
    
    team_ids = [3, 4]
    fields = "auton_score,high_goals"
    
    team_numbers = []
    for team_id in team_ids:
        team = Team.objects.get(id=team_id)
        team_numbers.append(team.teamNumber)
    
    context = {"team_ids": ",".join(str(x) for x in team_ids),
               "team_numbers": team_numbers,
               "field_list": fields,
              }
    
    return render(request, 'Scouting2013/view_graph.html', context)


def create_metrics_plot(request, team_ids, fields):
    
    team_ids = [str(x) for x in team_ids.split(",")]
    fields = [str(x) for x in fields.split(",")]    
    
    f = plt.figure(figsize=(6,6))
    legend_handles = []
    
    for team_id in team_ids:
        team = Team.objects.get(id=team_id)
        
        for field in fields:
            metric = []
            for result in team.scoreresult_set.all():
                metric.append(getattr(result, field))
            print field
            hand, = plt.plot(metric, label="Team %s, %s" % (team.teamNumber, field))
            legend_handles.append(hand)
            
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(handles=legend_handles, prop=fontP)
    plt.xlabel("Match")
    
    matplotlib.pyplot.close(f)
    
    canvas = FigureCanvasAgg(f)    
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    
    return response
