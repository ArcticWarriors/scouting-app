from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login


def auth_login(request, **kargs):
    username = request.POST['username']
    password = request.POST['password']
    good_redirect = request.POST.get('next', '/2016/%s' % kargs['regional_code'])
    bad_redirect = 'Scouting2016:showLogin'
    print(good_redirect)

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(good_redirect)
        else:
            return HttpResponseRedirect(reverse(bad_redirect, args=kargs.values()))
    else:
        return HttpResponseRedirect(reverse(bad_redirect, args=kargs.values()))
