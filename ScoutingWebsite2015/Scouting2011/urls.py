'''
Created on Oct 9, 2015

@author: PJ
'''
from django.conf.urls import url
from django.views.generic.base import TemplateView
from Scouting2011 import views
import view.generic_views as generic_views
import view.gen_graph as gen_graph
import view.user_auth as user_auth


app_name = 'Scouting2011'
urlpatterns = [url(r'^(?P<regional_code>\w+)$', TemplateView.as_view(template_name="Scouting2011/index.html"), name='index'),


               # User Auth
               url(r'^(?P<regional_code>\w+)/showLogin/$', user_auth.showLogin, name='showLogin'),
               url(r'^(?P<regional_code>\w+)/log_user_out$', user_auth.log_user_out, name='log_user_out'),
               url(r'^(?P<regional_code>\w+)/auth_login$', user_auth.auth_login, name='auth_login'),

               # Generic Views
               url(r'^(?P<regional_code>\w+)/gen_graph/(?P<team_numbers>\w+(,\w+)*)/(?P<fields>\w+(,\w+)*)$', gen_graph.gen_graph, name='gen_graph'),
               url(r'^(?P<regional_code>\w+)/matches$', generic_views.AllMatchesView.as_view(), name='matches'),
               url(r'^(?P<regional_code>\w+)/add_team_comments/(?P<team_number>[0-9]+)$', generic_views.AddTeamCommentsView.as_view(), name='add_team_comments'),

               # 2011 Views
               url(r'^(?P<regional_code>\w+)/teams$', views.AllTeamsViews2011.as_view(), name='teams'),
               url(r'^(?P<regional_code>\w+)/teams/(?P<team_number>[0-9]+)$', views.SingleTeamView2011.as_view(), name='view_team'),
               url(r'^(?P<regional_code>\w+)/matches/(?P<match_number>[0-9]+)$', views.SingleMatchView2011.as_view(), name='view_match'),
               url(r'^(?P<regional_code>\w+)/upload_image$', views.AddTeamPictureView2011.as_view(), name='upload_image'),

               # Robot Info
               url(r'^(?P<regional_code>\w+)/robot_display$', TemplateView.as_view(template_name='Scouting2011/robot_info/overview.html'), name='robot_display'),
               url(r'^(?P<regional_code>\w+)/robot_display/software$', TemplateView.as_view(template_name='Scouting2011/robot_info/software.html'), name='robot_display_software'),
               url(r'^(?P<regional_code>\w+)/robot_display/scaling$', TemplateView.as_view(template_name='Scouting2011/robot_info/scaling.html'), name='robot_display_scaling'),
               url(r'^(?P<regional_code>\w+)/robot_display/overroller$', TemplateView.as_view(template_name='Scouting2011/robot_info/overroller.html'), name='robot_display_overroller'),
               url(r'^(?P<regional_code>\w+)/robot_display/drivetrain$', TemplateView.as_view(template_name='Scouting2011/robot_info/drivetrain.html'), name='robot_display_drivetrain'),

               # Normal Pages
               ]
