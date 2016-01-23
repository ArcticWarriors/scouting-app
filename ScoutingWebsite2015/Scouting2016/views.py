from django.shortcuts import render

# Create your views here.

def index(request):

    return render(request, 'Scouting2016/index.html')

def robot_display(request):
    return render(request, 'Scouting2016/RobotDisplay.html')