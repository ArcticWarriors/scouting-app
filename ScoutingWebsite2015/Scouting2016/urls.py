'''
Created on Oct 9, 2015

@author: PJ
'''
from django.conf.urls import url
from . import views


urlpatterns = [
               url(r'^$', views.index, name='index'),
                url(r'^robot_display$', views.robot_display, name='robot_display'),
                url (r'^view_team/(?P<team_number>[0-9]+)$', views.view_team, name = 'view_team'),
                url (r'^match_display/(?P<match_number>[0-9]+)$', views.match_display, name = 'match_display'),
                 url(r'^all_teams$', views.all_teams, name='all_teams'),
                 url(r'^all_matches$', views.all_matches, name='all_matches'),
              ]
