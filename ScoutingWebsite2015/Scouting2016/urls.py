'''
Created on Oct 9, 2015

@author: PJ
'''
from django.conf.urls import url
from . import views


app_name = 'Scouting2016'
urlpatterns = [
               url(r'^$', views.index, name='index'),
               
               #Add/Edit Form
               url(r'^form$', views.show_add_form, name='showForm'),
               url(r'^edit_form$', views.show_edit_form, name='show_edit_form'),
               url(r'^pre_edit_form', views.info_for_form_edit, name='info_for_form_edit'),
               url(r'^submit_form$', views.submit_new_match, name='show_add_form'),
               url(r'^submit_edit$', views.edit_prev_match, name='edit_form'),
               
               #Normal Pages
               url(r'^robot_display$', views.robot_display, name='robot_display'),
               url (r'^view_team/(?P<team_number>[0-9]+)$', views.view_team, name = 'view_team'),
               url (r'^match_display/(?P<match_number>[0-9]+)$', views.match_display, name = 'match_display'),
               url(r'^all_teams$', views.all_teams, name='all_teams'),
               url(r'^all_matches$', views.all_matches, name='all_matches'),
               url(r'^search$', views.search_page, name='search_page'),
               url(r'^search_results$', views.search_results, name='search_results'),
              ]

