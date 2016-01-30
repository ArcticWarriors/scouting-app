from django.shortcuts import render
from django.template.context_processors import request
from Scouting2016.models import Team, Match, ScoreResult
from django.db.models import Avg, Sum
from django.http.response import HttpResponse

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


def __get_create_kargs(request):
    
    kargs = {}
    
    score_result_fields_with_default= __get_score_result_fields()
    
    for field_name in score_result_fields_with_default:
        if field_name not in request.POST:
            kargs[field_name] = score_result_fields_with_default[field_name]
        else:
            kargs[field_name] = request.POST[field_name]
          
    return kargs
    

def index(request):
    
    return render(request, 'Scouting2016/index.html')

def show_graph(request):
    context = {}
    context['teams']=Team.objects.all()
    return render(request,'Scouting2016/showGraph.html',context)

def submit_graph(request):
    
    teams = []
    fields = []
    
    for key in request.GET:
        try:
            team_number = int(key)
            teams.append(team_number)
        except:
            fields.append(key)
            
    print teams
    print fields
    
    teams = ",".join(str(x) for x in teams)
    fields = ",".join(str(x) for x in fields)
    
    context = {}
    context['teams']=Team.objects.all()
    context['graph_url'] = 'gen_graph/%s/%s' % (teams, fields)
    return render(request,'Scouting2016/showGraph.html',context)

def gen_graph(request, team_numbers, fields):
    
    import matplotlib
    matplotlib.use('agg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.font_manager import FontProperties
    
    team_numbers = [int(x) for x in team_numbers.split(",")]
    fields = fields.split(',')
    
    
    f = plt.figure(figsize=(6,6))
    legend_handles = []
    
    print team_numbers
    print fields
    for team_number in team_numbers:
        print team_number
        team = Team.objects.get(teamNumber=int(team_number))
        
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
    
    pass

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

    this_match = Match.objects.get(matchNumber=match_number)
    
    score_result_list = []
    
    for sr in this_match.scoreresult_set.all():
        score_result_list.append(sr)
        
    context['score_result_list'] = score_result_list
    context['match_display'] = match_number
    return render(request, 'Scouting2016/MatchPage.html', context)


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
    matches = Match.objects.all()
    context = {}
    context['matches']=matches
    
    return render(request, 'Scouting2016/AllMatches.html',context)


def search_page(request):
    return render(request, 'Scouting2016/index.html')


#######################################
# Form Stuff
#######################################


def info_for_form_edit(request):
    
    return render(request, 'Scouting2016/info_for_form_edit.html')


def show_add_form(request):
    score_result = __get_score_result_fields()
    
    context = {}
    context['team_number'] = 1765
    context['match_number'] = 10
    context['submit_view'] = "/2016/submit_form"
    context["sr"] = score_result

    
    return render(request, 'Scouting2016/inputForm.html', context)


def show_edit_form(request):
    
    match = Match.objects.get(matchNumber=request.GET["match_number"])
    team = Team.objects.get(teamNumber=request.GET["team_number"])
    
    score_results = ScoreResult.objects.get(match_id=match.id, team_id=team.id)
    
    context = {}
    context['team_number'] = request.GET["team_number"]
    context['match_number'] = request.GET["match_number"]
    context['sr'] = score_results
    context['submit_view'] = '/2016/submit_edit'
    context['lock_team_and_match'] = True
    
    print "doing edit..."
    
    return render(request, 'Scouting2016/inputForm.html', context)

"""
Creates a new score result and match (if possible).  Uses the team and match number
from the form to search for an existing score result.  If one exists, it will
re-direct the user back to the form so they can attempt to input the data again.

If the score result does not exist, a new one will be created
"""
def submit_new_match(request):
    team = Team.objects.get(teamNumber=request.POST["team_number"])
    if len(Match.objects.filter(matchNumber=request.POST["match_number"])) == 0:
        match = Match.objects.create(matchNumber=request.POST["match_number"])
    else :
        match = Match.objects.get(matchNumber=request.POST["match_number"])
        
    available_srs = ScoreResult.objects.filter(match=match,  team=team)

    context = {}
    context['submit_view'] = "/2016/submit_form"
    render_view = 'Scouting2016/inputForm.html'
    
    # score result with this combination already exists, don't let them add it again
    if len(available_srs) != 0:
        context['error_message'] = "ERROR! A combination of team %s and match %s already exists" % (team.teamNumber, match.matchNumber)
        context['match_number'] = match.matchNumber
        context['team_number'] = team.teamNumber
        
        fake_score_result = {}
        for key in request.POST:
            fake_score_result[key] = request.POST[key]
        context['sr'] = fake_score_result
    else:
        render_view = 'Scouting2016/MatchPage.html'
        context['match_display'] = match.matchNumber
        kargs = __get_create_kargs(request)
        ScoreResult.objects.create(match=match, team=team, **kargs)
     
    return render(request, render_view, context)

"""
Edits an existing match.
"""
def edit_prev_match(request):
    match = Match.objects.get(matchNumber=request.POST["match_number"])
    team = Team.objects.get(teamNumber=request.POST["team_number"])
    
    score_result = ScoreResult.objects.get(match_id=match.id, team_id=team.id)
    
    sr_fields = request.POST
    for key, value in sr_fields.iteritems():
        setattr(score_result, key, value)
    score_result.save()
        
    context = {}
    context['match_display'] = match.matchNumber
    
    return render(request, 'Scouting2016/MatchPage.html', context)
    