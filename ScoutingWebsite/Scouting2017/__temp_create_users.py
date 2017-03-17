'''
Created on Feb 25, 2017

@author: PJ
'''

import sys
sys.path.append("..")

from BaseScouting.load_django import load_django
load_django()

from django.contrib.auth.models import User
from BaseScouting.load_django import load_django


def get_or_create(username, password, favorites, dnps):
    if len(User.objects.filter(username=username)) == 0:
        User.objects.create_user(username, password=password)

    from Scouting2017.model import Scout, Team
    user = User.objects.get(username=username)
    scout, _ = Scout.objects.get_or_create(user=user)

    for team_number in favorites:
        scout.bookmarked_teams.add(Team.objects.get(teamNumber=team_number))

    for team_number in dnps:
        scout.do_not_pick_teams.add(Team.objects.get(teamNumber=team_number))

    return user


load_django()
user = get_or_create('pjreiniger', 'pjreiniger', [174, 191], [1450])
user = get_or_create('starke', 'starke', [174, 1126, 340], [1450])
user = get_or_create('lee', 'lee', [174, 20, 1507], [])

user = get_or_create('progbot', 'progbot', [174, 1126, 1507], [])
user = get_or_create('wilson', 'wilson', [], [])
user = get_or_create('wong', 'wong', [], [])
user = get_or_create('dromms', 'dromms', [], [])
user = get_or_create('larham', 'larham', [], [])

user = get_or_create('goel', 'goel', [], [])
user = get_or_create('hussak', 'hussak', [], [])
user = get_or_create('taskovski', 'taskovski', [], [])
user = get_or_create('williams', 'williams', [], [])
user = get_or_create('nguyen', 'nguyen', [], [])
user = get_or_create('perrotta', 'perrotta', [], [])
user = get_or_create('johnson', 'johnson', [], [])
user = get_or_create('fenner', 'fenner', [], [])
