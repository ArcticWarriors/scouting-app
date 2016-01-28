from django.shortcuts import render
from django.template.context_processors import request
from Scouting2016.models import Team, Match, ScoreResult

# Create your views here.

def index(request):

    return render(request, 'Scouting2016/index.html')

def showForm(request):
    context = {}
    context['auto_score_high'] = 0
    context['auto_score_low'] = 0
    context['cheval_de_frise'] = 0
    context['draw_bridge'] = 0
    context['high_score_fail'] = 0
    context['high_score_successful'] = '0'
    context['low_bar'] = 0
    context['low_score_fail'] = 0
    context['low_score_successful'] = 0
    context['match_number'] = 1
    context['moat'] = 0
    context['notes_text_area'] = 0
    context['ramparts'] = 0
    context['rock_wall'] = 0
    context['rough_terrain'] = 0
    context['score_tech_foul'] = 0
    context['team_number'] = 2000
    
    context['sally_port'] = 0
    context['auto_defense'] = 'auto_cross_ramparts'
    context['auto_spy'] = 'auto_spy_yes'
    context['portcullis'] = 5
    context['scale_challenge'] = 'scale_partial'    
    context['slow_fast_bridge'] = 'slow_bridge'
    context['slow_fast_cheval'] = 'fast_cheval'
    context['slow_fast_low_bar'] = 'slow_low_bar'
    context['slow_fast_moat'] = 'slow_moat'
    context['slow_fast_portcullis'] = 'slow_portcullis'
    context['slow_fast_ramparts'] = 'no_move_ramparts'
    context['slow_fast_rock_wall'] = 'no_move_rock_wall'
    context['slow_fast_rough'] = 'slow_rough'
    context['slow_fast_sally'] = 'slow_sally'

    
    return render(request, 'Scouting2016/inputForm.html', context)

def robot_display(request):
    return render(request, 'Scouting2016/RobotDisplay.html')

def view_team(request, team_number):
    context = {}
    context['team_number'] = team_number
    return render(request, 'Scouting2016/TeamPage.html', context)

def match_display(request, match_number):
    context = {}
    context['match_display'] = match_number
    print context
    return render(request, 'Scouting2016/MatchPage.html', context)

def edit_form(request, team_number, match_number):
    
    match = Match.objects.get(matchNumber=match_number)
    team = Team.objects.get(teamNumber=team_number)
    
    score_results = ScoreResult.objects.get(match_id=match.id, team_id=team.id)
    
    context = {}
    context['team_number'] = team_number
    context['match_number'] = match_number
    
    context['auto_score_high'] = score_results.auto_score_high
    context['auto_score_low'] = score_results.auto_score_low
    context['cheval_de_frise'] = score_results.cheval_de_frise
    context['draw_bridge'] = score_results.draw_bridge
    context['high_score_fail'] = score_results.high_score_fail
    context['high_score_successful'] = score_results.high_score_successful
    context['low_bar'] = score_results.low_bar
    context['low_score_fail'] = score_results.low_score_fail
    context['low_score_successful'] = score_results.low_score_successful
    context['moat'] = score_results.moat
    context['notes_text_area'] = score_results.notes_text_area
    context['ramparts'] = score_results.ramparts
    context['rock_wall'] = score_results.rock_wall
    context['rough_terrain'] = score_results.rough_terrain
    context['score_tech_foul'] = score_results.score_tech_foul
    
    context['sally_port'] = score_results.sally_port
    context['auto_defense'] = score_results.auto_defense
    context['auto_spy'] = score_results.auto_spy
    context['portcullis'] = score_results.portcullis
    context['scale_challenge'] = score_results.scale_challenge    
    context['slow_fast_bridge'] = score_results.slow_fast_bridge
    context['slow_fast_cheval'] = score_results.slow_fast_cheval
    context['slow_fast_low_bar'] = score_results.slow_fast_low_bar
    context['slow_fast_moat'] = score_results.slow_fast_moat
    context['slow_fast_portcullis'] = score_results.slow_fast_portcullis
    context['slow_fast_ramparts'] = score_results.slow_fast_ramparts
    context['slow_fast_rock_wall'] = score_results.slow_fast_rock_wall
    context['slow_fast_rough'] = score_results.slow_fast_rough
    context['slow_fast_sally'] = score_results.slow_fast_sally
    return render(request, 'Scouting2016/inputForm.html', context)


#Change^^^^^
def all_teams(request):
    return render(request, 'Scouting2016/AllTeams.html')

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
                                              notes_text_area = request.POST["notes_text_area"],
                                              #New Stuff that needs to updated to the Model 
                                              auto_spy = request.POST["auto_spy"],
                                              portcullis = request.POST["portcullis"],
                                              auto_defense = request.POST["auto_defense"],
                                              scale_challenge = request.POST["scale_challenge"],
                                              slow_fast_low_bar = request.POST["slow_fast_low_bar"],
                                              slow_fast_moat = request.POST["slow_fast_moat"],
                                              slow_fast_rock_wall = request.POST["slow_fast_rock_wall"],
                                              slow_fast_rough = request.POST["slow_fast_rough"],
                                              slow_fast_ramparts = request.POST["slow_fast_ramparts"],
                                              slow_fast_portcullis = request.POST["slow_fast_portcullis"],
                                              slow_fast_sally = request.POST["slow_fast_sally"],
                                              slow_fast_bridge = request.POST["slow_fast_bridge"],
                                              slow_fast_cheval = request.POST["slow_fast_cheval"],)
        
    print "Adding SR: %s, %s" % (team, match)   
    return render(request, 'Scouting2016/index.html')