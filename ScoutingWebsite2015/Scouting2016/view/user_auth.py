'''
Created on Mar 28, 2016

@author: PJ
'''
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout


def showLogin(request, **kargs):

    return render(request, 'Scouting2016/login.html', context=kargs)


def log_user_out(request, **kargs):
    logout(request)

    return HttpResponseRedirect(reverse('Scouting2016:showLogin', args=kargs.values()))


def auth_login(request, **kargs):
    username = request.POST['username']
    password = request.POST['password']
    good_redirect = request.POST.get('next', '/2016/%s' % kargs['regional_code'])
    bad_redirect = 'Scouting2016:showLogin'
    print good_redirect

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(good_redirect)
        else:
            return HttpResponseRedirect(reverse(bad_redirect, args=kargs.values()))
    else:
        return HttpResponseRedirect(reverse(bad_redirect, args=kargs.values()))
