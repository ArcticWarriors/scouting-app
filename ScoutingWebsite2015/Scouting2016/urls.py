'''
Created on Oct 9, 2015

@author: PJ
'''
from django.conf.urls import url
from . import views


app_name = 'Scouting2016'
urlpatterns = [
               url(r'^$', views.index, name='index'),
               url(r'^form$', views.showForm, name='showForm'),
               url(r'^submit_form$', views.submitForm, name='submit_form'),
               url(r'^robot_display$', views.robot_display, name='robot_display'),
               url (r'^view_team/(?P<team_number>[0-9]+)$', views.view_team, name = 'view_team'),
               url (r'^match_display/(?P<match_number>[0-9]+)$', views.match_display, name = 'match_display'),
               url(r'^all_teams$', views.all_teams, name='all_teams'),
               url(r'^all_matches$', views.all_matches, name='all_matches'),
               url(r'^match_(?P<match_number>[0-9]+)/team_(?P<team_number>[0-9]+)$', views.edit_form, name='edit_form'),
              ]
