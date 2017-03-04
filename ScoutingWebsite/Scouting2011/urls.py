'''
Created on Oct 9, 2015

@author: PJ
'''
from django.conf.urls import url
from django.views.generic.base import TemplateView, RedirectView
import Scouting2011.view.standard_views as standard_views
from Scouting2011.view.standard_views.homepage import HomepageView2011
from Scouting2011.view.standard_views.match import SingleMatchView2011
from Scouting2011.view.standard_views.team import SingleTeamView2011
from Scouting2011.view.standard_views.match_list import AllMatchesView2011
from Scouting2011.view.standard_views.team_list import AllTeamsViews2011
from Scouting2011.view.submission.add_team_picture import AddTeamPictureView2011
from Scouting2011.view.submission.add_team_comments import AddTeamCommentsView2011
from Scouting2011.view.standard_views.match_prediction import OfficialMatchView2011

app_name = 'Scouting2011'
urlpatterns = [
               url(r'^$', RedirectView.as_view(url='/2011/NYLI', permanent=False)),
               url(r'^(?P<regional_code>\w+)$', HomepageView2011.as_view(), name='index'),


               # 2011 Views
               url(r'^(?P<regional_code>\w+)/teams$', AllTeamsViews2011.as_view(), name='teams'),
               url(r'^(?P<regional_code>\w+)/teams/(?P<team_number>[0-9]+)$', SingleTeamView2011.as_view(), name='view_team'),
               url(r'^(?P<regional_code>\w+)/matches$', AllMatchesView2011.as_view(), name='matches'),
               url(r'^(?P<regional_code>\w+)/matches/(?P<match_number>[0-9]+)$', SingleMatchView2011.as_view(), name='view_match'),
               url(r'^(?P<regional_code>\w+)/upload_image$', AddTeamPictureView2011.as_view(), name='upload_image'),
#                url(r'^(?P<regional_code>\w+)/gen_graph/(?P<team_numbers>\w+(,\w+)*)/(?P<fields>\w+(,\w+)*)$', GenGraphView2011.as_view(), name='gen_graph'),
               url(r'^(?P<regional_code>\w+)/add_team_comments/(?P<team_number>[0-9]+)$', AddTeamCommentsView2011.as_view(), name='add_team_comments'),
               url(r'^(?P<regional_code>\w+)/match_prediction/(?P<match_number>[0-9]+)$', OfficialMatchView2011.as_view(), name='match_prediction'),

               # Robot Info
               url(r'^(?P<regional_code>\w+)/robot_display$', TemplateView.as_view(template_name='Scouting2011/robot_info/overview.html'), name='robot_display'),
               
               # User Auth
               url(r'^(?P<regional_code>\w+)/showLogin/$', HomepageView2011.as_view(), name='show_login'),
               url(r'^(?P<regional_code>\w+)/log_user_out$', HomepageView2011.as_view(), name='log_user_out'),
               url(r'^(?P<regional_code>\w+)/auth_login$', HomepageView2011.as_view(), name='auth_login'),
               ]
