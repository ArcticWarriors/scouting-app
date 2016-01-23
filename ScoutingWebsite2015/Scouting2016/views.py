from django.shortcuts import render

# Create your views here.

def index(request):

    return render(request, 'Scouting2016/index.html')

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

def all_teams(request):
    return render(request, 'Scouting2016/AllTeams.html')

def all_matches(request):
    return render(request, 'Scouting2016/AllMatches.html')