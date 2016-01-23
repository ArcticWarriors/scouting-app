'''
Created on Oct 9, 2015

@author: PJ
'''
from django.conf.urls import url
from . import views


urlpatterns = [
               url(r'^$', views.index, name='index'),
               url(r'^teams$', views.all_teams, name='all_teams'),
               url(r'^teams/(?P<team_id>[0-9]+)$', views.view_team, name='view_team'),
               url(r'^match$', views.all_matches, name='all_matches'),
               url(r'^match/(?P<match_id>[0-9]+)$', views.view_match, name='view_match'),
               url(r'^view_graph$', views.view_graph, name='view_graph'),
               url(r'^create_metrics_plot/teams=(?P<team_ids>\w+(,\w+)*),fields=(?P<fields>\w+(,\w+)*)', views.create_metrics_plot, name='create_metrics_plot'),
              ]
