from django.shortcuts import render


def show_login(request, **kargs):

    return render(request, 'BaseScouting/login.html', context=kargs)
