from django.contrib.auth import logout
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse


def log_user_out(request, **kargs):
    logout(request)

    return HttpResponseRedirect(reverse('Scouting2017:show_login', args=kargs.values()))
