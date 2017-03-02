from django.contrib.auth.decorators import permission_required
from Scouting2016.model.models2016 import ScoreResult
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy


@permission_required('auth.can_modify_model', login_url=reverse_lazy('Scouting2016:showLogin'))
def show_add_form(request, regional_code):

    context = {}
    context['regional_code'] = regional_code
    context['submit_view'] = "/2016/%s/submit_form" % regional_code
    context["sr"] = {}

    score_result_fields = ScoreResult.get_fields()
    for field_name, value in score_result_fields.iteritems():
        context["sr"][field_name] = value.default

    return render(request, 'Scouting2016/match_form/match_form.html', context)
