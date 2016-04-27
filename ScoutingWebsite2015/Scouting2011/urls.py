'''
Created on Oct 9, 2015

@author: PJ
'''
from django.conf.urls import url
from django.views.generic.base import TemplateView
import view.standard_views as standard_views

app_name = 'Scouting2011'
urlpatterns = [url(r'^(?P<regional_code>\w+)$', TemplateView.as_view(template_name="Scouting2011/index.html"), name='index'),


               # 2011 Views
               url(r'^(?P<regional_code>\w+)/teams$', standard_views.AllTeamsViews2011.as_view(), name='teams'),
               url(r'^(?P<regional_code>\w+)/teams/(?P<team_number>[0-9]+)$', standard_views.SingleTeamView2011.as_view(), name='view_team'),
               url(r'^(?P<regional_code>\w+)/matches$', standard_views.AllMatchesView2011.as_view(), name='matches'),
               url(r'^(?P<regional_code>\w+)/matches/(?P<match_number>[0-9]+)$', standard_views.SingleMatchView2011.as_view(), name='view_match'),
               url(r'^(?P<regional_code>\w+)/upload_image$', standard_views.AddTeamPictureView2011.as_view(), name='upload_image'),
               url(r'^(?P<regional_code>\w+)/gen_graph/(?P<team_numbers>\w+(,\w+)*)/(?P<fields>\w+(,\w+)*)$', standard_views.GenGraphView2011.as_view(), name='gen_graph'),
               url(r'^(?P<regional_code>\w+)/add_team_comments/(?P<team_number>[0-9]+)$', standard_views.AddTeamCommentsView2011.as_view(), name='add_team_comments'),

               # Robot Info
               url(r'^(?P<regional_code>\w+)/robot_display$', TemplateView.as_view(template_name='Scouting2011/robot_info/overview.html'), name='robot_display'),
               ]
