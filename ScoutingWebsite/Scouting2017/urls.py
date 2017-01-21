'''
Created on Jan 15, 2017

@author: PJ
'''
from django.conf.urls import url
from django.views.generic.base import RedirectView
from Scouting2017.view import standard_views


app_name = 'Scouting2017'
urlpatterns = [
    
               url(r'^$', RedirectView.as_view(url='/2017/NYRO', permanent=False)),
               url(r'^(?P<regional_code>\w+)$', standard_views.HomepageView2017.as_view(), name='index'),
               url(r'^(?P<regional_code>\w+)/teams$', standard_views.AllTeamsViews2017.as_view(), name='teams'),
               url(r'^(?P<regional_code>\w+)/matches$', standard_views.AllMatchesViews2017.as_view(), name='matches'),
               url(r'^(?P<regional_code>\w+)/teams/(?P<team_number>[0-9]+)$', standard_views.SingleTeamView2017.as_view(), name='view_team'),
               
               
               ]