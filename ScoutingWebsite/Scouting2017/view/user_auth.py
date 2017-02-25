'''
Created on Mar 28, 2016

@author: PJ
'''
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User


def show_login(request, **kargs):

    return render(request, 'BaseScouting/login.html', context=kargs)


def log_user_out(request, **kargs):
    logout(request)

    return HttpResponseRedirect(reverse('Scouting2017:show_login', args=kargs.values()))


def auth_login(request, **kargs):
    username = request.POST['username']
    password = request.POST['password']
    good_redirect = request.POST.get('next', '/2017/%s' % kargs['regional_code'])
    bad_redirect = 'Scouting2017:show_login'
    
    success = False

    try:
        User.objects.get(username=username)
        
        user = authenticate(username=username, password=password)
#         print user, user.is_active
        if user is not None:
            print user.is_active
            if user.is_active:
                login(request, user)
                success = True
        else:
            messages.add_message(request, messages.ERROR, "Username and password do not match for %s" % username)
#                 return HttpResponseRedirect(reverse(bad_redirect, args=kargs.values()))
    
    except Exception as e:
        print e
        messages.add_message(request, messages.ERROR, "Username %s was not found" % username)
        
    if success:
        return HttpResponseRedirect(good_redirect)
    else:
        return HttpResponseRedirect(reverse(bad_redirect, args=kargs.values()))
