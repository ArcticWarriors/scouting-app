from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect


def log_user_out(request, **kargs):
    logout(request)

    return HttpResponseRedirect(reverse('Scouting2016:showLogin', args=kargs.values()))
