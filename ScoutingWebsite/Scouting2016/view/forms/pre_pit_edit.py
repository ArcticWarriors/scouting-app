from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render


@permission_required('auth.can_modify_model', login_url=reverse_lazy('Scouting2016:showLogin'))
def info_for_pit_edit(request, regional_code):
    return render(request, 'Scouting2016/pit_form/pre_pit_form.html', context={'regional_code': regional_code})
