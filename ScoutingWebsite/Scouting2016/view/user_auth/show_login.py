from django.shortcuts import render


def showLogin(request, **kargs):

    return render(request, 'Scouting2016/login.html', context=kargs)
