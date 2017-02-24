'''
Created on Feb 22, 2017

@author: PJ
'''
from Scouting2017.model.reusable_models import Competition, Team, Match
from Scouting2017.model.models2017 import ScoreResult
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from BaseScouting.views.base_views import BaseMatchEntryView
from django.utils.decorators import method_decorator


login_reverse = reverse_lazy('Scouting2017:show_login')


class MatchEntryView2017(BaseMatchEntryView):
    def __init__(self):
        BaseMatchEntryView.__init__(self, 'Scouting2017/match_entry.html')

    @method_decorator(permission_required('auth.can_modify_model', login_url=login_reverse))
    def dispatch(self, *args, **kwargs):
        return super(MyModelDeleteView, self).dispatch(*args, **kwargs)


@permission_required('auth.xxx', login_url=login_reverse)
def add_match(request, regional_code):
    
    print regional_code
    post = request.POST
    num_rows = int(post['rowCounter'])
    for i in range(num_rows):
        comp = Competition.objects.get(code=regional_code)
        team = Team.objects.get_or_create(teamNumber=int(post['teamNumber-%s' % (i + 1)]))[0]
        match = Match.objects.get_or_create(competition=comp, matchNumber=int(post['matchNumber-%s' % (i + 1)]))[0]
        
        ropeclimbed = 'ropeClimbed-%s' % (i + 1) in post
        auto_baseline = 'autoBaseline-%s' % (i + 1) in post
        auto_gear_scored = 'autoGear-%s' % (i+1) in post
        defensive_play = 'defesnive-%s' % (i+1) in post
        
        print ropeclimbed
        
        score_result = ScoreResult.objects.create(
            competition = comp,
            team = team,
            match = match,
            gears_score = int(post['gearScore-%s' % (i + 1)]),
            fuel_shot_hi = int(post['highFuelShot-%s' % (i + 1)]),
            fuel_shot_low = int(post['lowFuelShot-%s' % (i + 1)]),
            fuel_score_hi = int(post['highFuelScore-%s' % (i + 1)]),
            fuel_score_low = int(post['lowFuelScore-%s' % (i + 1)]),
            rope = bool(ropeclimbed),
#             hopper = individual_data['    hopper'],
#              tech_foul = individual_data['    tech_foul'],
#             foul = individual_data['    foul'],
#             red_card = individual_data['    red_card'],
#             yellow_card = individual_data['    yellow_card'],
#             fuel_shot_hi_auto = individual_data['    fuel_shot_hi_auto'],
#             fuel_shot_low_auto = individual_data['    fuel_shot_low_auto'],
#             fuel_score_hi_auto = individual_data['    fuel_score_hi_auto'],
#             fuel_score_low_auto = individual_data['    fuel_score_low_auto'],
#             gears_score_auto = individual_data['    gears_score_auto'],
            baseline = bool(auto_baseline),
            scored_gear_in_auto = bool(auto_gear_scored),
#             defensive = bool(defensive_play),
#             ground_fuel = individual_data['    ground_fuel'],
#             ground_gear = individual_data['    ground_gear'],
        )
        score_result.save()
        
    return HttpResponseRedirect(reverse('Scouting2017:index', args=(regional_code,)))
