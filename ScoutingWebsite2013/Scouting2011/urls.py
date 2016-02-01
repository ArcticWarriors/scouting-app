'''
Created on Oct 9, 2015

@author: PJ
'''
from django.conf.urls import url
from . import views


urlpatterns = [url(r'^$', views.index, name='index'),

               # Normal Pages
               url(r'^robot_display$', views.robot_display, name='robot_display'),
               url(r'^view_team/(?P<team_number>[0-9]+)$', views.view_team, name='view_team'),
               url(r'^match_display/(?P<match_number>[0-9]+)$', views.match_display, name='match_display'),
               url(r'^all_teams$', views.all_teams, name='all_teams'),
               url(r'^all_matches$', views.all_matches, name='all_matches'),
               url(r'^search$', views.search_page, name='search_page'),
               url(r'^graph$', views.show_graph, name='show_graph'),
               url(r'^gen_graph/(?P<team_numbers>\w+(,\w+)*)/(?P<fields>\w+(,\w+)*)$', views.gen_graph, name='gen_graph'),
               ]
