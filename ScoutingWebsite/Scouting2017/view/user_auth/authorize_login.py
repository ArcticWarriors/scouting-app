
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User


def auth_login(request, **kargs):
    username = request.POST['username']
    password = request.POST['password']
    good_redirect = request.POST.get('next', '/2017/%s' % kargs['regional_code'])
    bad_redirect = 'Scouting2017:show_login'

    success = False

    try:
        User.objects.get(username=username)

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                success = True
        else:
            messages.add_message(request, messages.ERROR, "Username and password do not match for %s" % username)
#                 return HttpResponseRedirect(reverse(bad_redirect, args=kargs.values()))

    except Exception as e:
        print "Exception %s" % e
        messages.add_message(request, messages.ERROR, "Username %s was not found" % username)

    if success:
        return HttpResponseRedirect(good_redirect)
    else:
        return HttpResponseRedirect(reverse(bad_redirect, args=kargs.values()))
