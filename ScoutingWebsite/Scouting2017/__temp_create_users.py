'''
Created on Feb 25, 2017

@author: PJ
'''

import sys
from django.contrib.contenttypes.models import ContentType
sys.path.append("..")

from BaseScouting.load_django import load_django
load_django()

from django.contrib.auth.models import User, Group, Permission
from BaseScouting.load_django import load_django


def create_groups():

    abilities = {}
    abilities["picklist"] = {"app_label": "Scouting2017", "model": "picklist", "abilities": ["add", "change"]}
    abilities["teamcomments"] = {"app_label": "Scouting2017", "model": "teamcomments", "abilities": ["add", "change"]}
    abilities["teampictures"] = {"app_label": "Scouting2017", "model": "teampictures", "abilities": ["add", "change"]}
    abilities["teampitscouting"] = {"app_label": "Scouting2017", "model": "teampitscouting", "abilities": ["add", "change"]}
    abilities["scoreresult"] = {"app_label": "Scouting2017", "model": "scoreresult", "abilities": ["add", "change"]}
    all_abilities = [x for x in abilities.values()]

    groups_permissions = {}
    groups_permissions["scout"] = [abilities["teamcomments"], abilities["scoreresult"], abilities["teampitscouting"], abilities["teampictures"]]
    groups_permissions["driver"] = [abilities["teamcomments"]]
    groups_permissions["scout_master"] = all_abilities
    groups_permissions["admin"] = all_abilities

    for group_name in groups_permissions:
        group_abilities = groups_permissions[group_name]

        group, _ = Group.objects.get_or_create(name=group_name)

        for ability in group_abilities:
            model = ability['model']
            content_type = ContentType.objects.get(app_label=ability['app_label'], model=model)

            for ability_type in ability["abilities"]:
                permission = Permission.objects.get(content_type=content_type, codename=ability_type + "_" + model)
                group.permissions.add(permission)


def get_or_create_user(username, password, groups, favorites, dnps):
    if len(User.objects.filter(username=username)) == 0:
        User.objects.create_user(username, password=password)

    from Scouting2017.model import Scout, Team
    user = User.objects.get(username=username)
    scout, _ = Scout.objects.get_or_create(user=user)

    for team_number in favorites:
        scout.bookmarked_teams.add(Team.objects.get(teamNumber=team_number))

    for team_number in dnps:
        scout.do_not_pick_teams.add(Team.objects.get(teamNumber=team_number))

    for group in groups:
        group = Group.objects.get(name=group)
        group.user_set.add(user)

    return user


create_groups()

load_django()
user = get_or_create_user('pjreiniger', 'pjreiniger', ["admin", "scout_master"], [174, 191], [1450])
user = get_or_create_user('starke', 'starke', ["scout_master"], [174, 1126, 340], [1450])
user = get_or_create_user('lee', 'lee', ["scout_master"], [174, 20, 1507], [])

user = get_or_create_user('progbot', 'progbot', ["admin", "scout", "scout_master"], [174, 1126, 1507], [])
user = get_or_create_user('wilson', 'wilson', ["scout"], [], [])
user = get_or_create_user('wong', 'wong', ["scout"], [], [])
user = get_or_create_user('dromms', 'dromms', ["scout", "scout_master"], [], [])
user = get_or_create_user('larham', 'larham', ["scout"], [], [])

user = get_or_create_user('goel', 'goel', ["driver"], [], [])
user = get_or_create_user('hussak', 'hussak', ["driver"], [], [])
user = get_or_create_user('taskovski', 'taskovski', ["driver"], [], [])
user = get_or_create_user('williams', 'williams', ["driver"], [], [])
user = get_or_create_user('nguyen', 'nguyen', ["driver"], [], [])
user = get_or_create_user('perrotta', 'perrotta', ["scout"], [], [])
user = get_or_create_user('johnson', 'johnson', ["scout"], [], [])
user = get_or_create_user('fenner', 'fenner', ["scout"], [], [])
