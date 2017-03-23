'''
Created on Feb 25, 2017

@author: PJ
'''

import sys
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission
sys.path.append("..")

from BaseScouting.load_django import load_django
load_django()


def create_groups():

    permissions_info = {}
    permissions_info["AddScoreResult"] = {"model": "scoreresult", "abilities": "add"}
    permissions_info["AddTeamComments"] = {"model": "teamcomments", "abilities": "add"}
    permissions_info["AddTeamPicture"] = {"model": "teampictures", "abilities": "add"}
    permissions_info["ModifyPitScouting"] = {"model": "teampitscouting", "abilities": "change"}
    permissions_info["ModifyScoreResult"] = {"model": "scoreresult", "abilities": "change"}
    permissions_info["ModifyPickList"] = {"model": "picklist", "abilities": "change"}

    permissions = {}

    for permission_name, permission_info in permissions_info.items():

        content_types = ContentType.objects.filter(model=permission_info['model'])

        permissions[permission_name] = []
        for content_type in content_types:
            permission, _ = Permission.objects.get_or_create(codename=permission_name, content_type=content_type)
            permissions[permission_name].append(permission)

    all_permissions = [x for x in permissions.values()]

    groups_permissions = {}
    groups_permissions["scout"] = [permissions["AddScoreResult"], permissions["AddTeamComments"], permissions["AddTeamPicture"], permissions["ModifyPitScouting"], permissions["ModifyScoreResult"]]
    groups_permissions["driver"] = [permissions["AddTeamComments"]]
    groups_permissions["scout_master"] = all_permissions
    groups_permissions["admin"] = all_permissions
#
    for group_name in groups_permissions:
        group, _ = Group.objects.get_or_create(name=group_name)
#
        for permissions in groups_permissions[group_name]:
            for permission in permissions:
                group.permissions.add(permission)


def get_or_create_user(username, password, team_number, groups, favorites, dnps):
    if len(User.objects.filter(username=username)) == 0:
        User.objects.create_user(username, password=password)

    from Scouting2017.model import Scout, Team
    user = User.objects.get(username=username)
    scouts_team = Team.objects.get(teamNumber=team_number)
    scout, _ = Scout.objects.get_or_create(user=user, team=scouts_team)

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
user = get_or_create_user('pjreiniger', 'pjreiniger', 174, ["admin", "scout_master"], [174, 191], [1450])
user = get_or_create_user('starke', 'starke', 174, ["scout_master"], [174, 1126, 340], [1450])
user = get_or_create_user('lee', 'lee', 174, ["scout_master"], [174, 20, 1507], [])

user = get_or_create_user('progbot', 'progbot', 174, ["admin", "scout", "scout_master"], [174, 1126, 1507], [])
user = get_or_create_user('wilson', 'wilson', 174, ["scout"], [], [])
user = get_or_create_user('wong', 'wong', 174, ["scout"], [], [])
user = get_or_create_user('dromms', 'dromms', 174, ["scout", "scout_master"], [], [])
user = get_or_create_user('larham', 'larham', 174, ["scout"], [], [])

user = get_or_create_user('goel', 'goel', 174, ["driver"], [], [])
user = get_or_create_user('hussak', 'hussak', 174, ["driver"], [], [])
user = get_or_create_user('taskovski', 'taskovski', 174, ["driver"], [], [])
user = get_or_create_user('williams', 'williams', 174, ["driver"], [], [])
user = get_or_create_user('nguyen', 'nguyen', 174, ["driver"], [], [])
user = get_or_create_user('perrotta', 'perrotta', 174, ["scout"], [], [])
user = get_or_create_user('johnson', 'johnson', 174, ["scout"], [], [])
user = get_or_create_user('fenner', 'fenner', 174, ["scout"], [], [])

#user = get_or_create_user('guest', 'guest', 174, [], [], [])
