from django.shortcuts import render
from django.template.context_processors import request

# Create your views here.

def index(request):

    return render(request, 'Scouting2016/index.html')

def showForm(request):

    return render(request, 'Scouting2016/inputForm.html')

def submitForm(request):
    print "Submitting Form"
    print request.POST
    return render(request, 'Scouting2016/index.html')