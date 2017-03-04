'''
Created on Oct 9, 2015

@author: PJ
'''
from django.conf.urls import url
from django.views.generic.base import TemplateView, RedirectView
import Scouting2013.view.standard_views as standard_views
from Scouting2013.view.standard_views.team_list import AllTeamsViews2013
from Scouting2013.view.standard_views.homepage import HomepageView2013
from Scouting2013.view.standard_views.team import SingleTeamView2013
from Scouting2013.view.standard_views.match_list import AllMatchesView2013
from Scouting2013.view.standard_views.match import SingleMatchView2013
from Scouting2013.view.submissions.add_team_pictures import AddTeamPictureView2013
from Scouting2013.view.submissions.add_team_comments import AddTeamCommentsView2013
from BaseScouting.views.base_views import BaseGenGraphView


app_name = 'Scouting2013'
urlpatterns = [
               url(r'^$', RedirectView.as_view(url='/2013/OHCL', permanent=False)),
               url(r'^(?P<regional_code>\w+)$', HomepageView2013.as_view(), name='index'),

               # 2013 Views
               url(r'^(?P<regional_code>\w+)/teams$', AllTeamsViews2013.as_view(), name='teams'),
               url(r'^(?P<regional_code>\w+)/teams/(?P<team_number>[0-9]+)$', SingleTeamView2013.as_view(), name='view_team'),
               url(r'^(?P<regional_code>\w+)/matches$', AllMatchesView2013.as_view(), name='matches'),
               url(r'^(?P<regional_code>\w+)/matches/(?P<match_number>[0-9]+)$', SingleMatchView2013.as_view(), name='view_match'),
               url(r'^(?P<regional_code>\w+)/upload_image$', AddTeamPictureView2013.as_view(), name='upload_image'),
               url(r'^(?P<regional_code>\w+)/gen_graph/(?P<team_numbers>\w+(,\w+)*)/(?P<fields>\w+(,\w+)*)$', BaseGenGraphView.as_view(), name='gen_graph'),
               url(r'^(?P<regional_code>\w+)/add_team_comments/(?P<team_number>[0-9]+)$', AddTeamCommentsView2013.as_view(), name='add_team_comments'),

               # Robot Info
               url(r'^(?P<regional_code>\w+)/robot_display$', TemplateView.as_view(template_name='Scouting2013/robot_info/overview.html'), name='robot_display'),
               ]
