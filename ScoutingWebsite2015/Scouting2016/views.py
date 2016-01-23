from django.shortcuts import render
from django.template.context_processors import request
from Scouting2016.models import Team, Match, ScoreResult

# Create your views here.

def index(request):

    return render(request, 'Scouting2016/index.html')

def showForm(request):

    return render(request, 'Scouting2016/inputForm.html')

def robot_display(request):
    return render(request, 'Scouting2016/RobotDisplay.html')

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