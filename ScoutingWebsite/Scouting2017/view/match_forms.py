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


class MatchEntryView2017(BaseMatchEntryView):
    def __init__(self):
        BaseMatchEntryView.__init__(self, 'Scouting2017/match_entry.html')


def add_match(request, regional_code):
    
    print regional_code
    post = request.POST
    num_rows = int(post['rowCounter'])
    for i in range(num_rows):
        comp = Competition.objects.get(code=regional_code)
        team = Team.objects.get(teamNumber=int(post['teamNumber-%s' % (i + 1)]))
        match = Match.objects.get(competition=comp, matchNumber=int(post['matchNumber-%s' % (i + 1)]))
        
        rope_climbed = 'ropeClimbed-%s' % (i + 1) in post
        auto_baseline = 'autoBaseline-%s' % (i + 1) in post
        auto_gear_scored = 'autoGear-%s' % (i+1) in post
        defensive_play = 'defesnive-%s' % (i+1) in post

        score_result = ScoreResult.objects.create(
            competition=comp,
            team=team,
            match=match,
            
            # Auto
            fuel_score_hi_auto=int(post['autoFuelHigh-%s' % (i + 1)]),
            fuel_score_low_auto=int(post['autoFuelLow-%s' % (i + 1)]),
            gears_score_auto=int(post['autoGears-%s' % (i + 1)]),
            baseline=auto_baseline,
            #scored_gear_in_auto = models.BooleanField(default=False)
            
            # Tele-op
            gears_score=int(post['teleGears-%s' % (i + 1)]),
            fuel_shot_hi=int(post['teleFuelHighShot-%s' % (i + 1)]),
            fuel_shot_low=int(post['teleFuelLowShot-%s' % (i + 1)]),
            fuel_score_hi=int(post['teleFuelHighScore-%s' % (i + 1)]),
            fuel_score_low=int(post['teleFuelLowScore-%s' % (i + 1)]),
            
            # Endgame
            rope=rope_climbed,
            
            # Fouls
            tech_foul=0,
            foul=0,
            red_card=0,
            yellow_card=0,
        )
        score_result.save()
        
    raise
        
    return HttpResponseRedirect(reverse('Scouting2017:index', args=(regional_code,)))
