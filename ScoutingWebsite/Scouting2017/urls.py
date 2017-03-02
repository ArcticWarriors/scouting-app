'''
Created on Jan 15, 2017

@author: PJ
'''
from django.conf.urls import url
from django.views.generic.base import RedirectView
from Scouting2017.view import standard_views
from Scouting2017.view.forms import create_match
from Scouting2017.api_scraper_TheBlueAlliance import tba_webook
from Scouting2017.view.submissions.submit_pit_scouting import submit_pit_scouting
from Scouting2017.view.submissions.submit_bookmark import update_bookmark
from Scouting2017.view.submissions.submit_match_edit import submit_match_edit
from Scouting2017.view.submissions.submit_match import add_match
from Scouting2017.view.standard_views.homepage import HomepageView2017
from Scouting2017.view.standard_views.team_list import TeamListView2017
from Scouting2017.view.standard_views.match_list import MatchListView2017
from Scouting2017.view.standard_views.match import SingleMatchView2017
from Scouting2017.view.standard_views.team import SingleTeamView2017
from Scouting2017.view.standard_views.pick_list import PickListView2017
from Scouting2017.view.user_auth.show_login import show_login
from Scouting2017.view.user_auth.log_user_out import log_user_out
from Scouting2017.view.user_auth.authorize_login import auth_login
from Scouting2017.view.forms.add_team_pics import AddTeamPictureView2017
from Scouting2017.view.standard_views.match_prediction import MatchPredictionView2017


app_name = 'Scouting2017'
urlpatterns = [
               # TBA Webhook
               url(r'^tba_webhook$', tba_webook.tba_webook, name='tba_webhook'),

               # Standard Views
               url(r'^$', RedirectView.as_view(url='/2017/NYRO', permanent=False)),
               url(r'^(?P<regional_code>\w+)$', HomepageView2017.as_view(), name='index'),
               url(r'^(?P<regional_code>\w+)/teams$', TeamListView2017.as_view(), name='teams'),
               url(r'^(?P<regional_code>\w+)/matches$', MatchListView2017.as_view(), name='matches'),
               url(r'^(?P<regional_code>\w+)/matches/(?P<match_number>[0-9]+)$', SingleMatchView2017.as_view(), name='view_match'),
               url(r'^(?P<regional_code>\w+)/teams/(?P<team_number>[0-9]+)$', SingleTeamView2017.as_view(), name='view_team'),
               url(r'^(?P<regional_code>\w+)/match_prediction/(?P<match_number>[0-9]+)$', MatchPredictionView2017.as_view(), name='match_prediction'),
               url(r'^(?P<regional_code>\w+)/pick_list$', PickListView2017.as_view(), name='pick_list'),

               # Forms
               url(r'^(?P<regional_code>\w+)/match_entry$', create_match.MatchEntryView2017.as_view(), name='match_entry'),
               url(r'^(?P<regional_code>\w+)/submit_new_match$', add_match, name='submit_new_match'),
               url(r'^(?P<regional_code>\w+)/submit_pit_scouting$', submit_pit_scouting, name='submit_pit_scouting'),
               url(r'^(?P<regional_code>\w+)/upload_image$', AddTeamPictureView2017.as_view(), name='upload_image'),
               url(r'^(?P<regional_code>\w+)/update_bookmark$', update_bookmark, name='update_bookmark'),
               url(r'^(?P<regional_code>\w+)/submit_match_edit$', submit_match_edit, name='submit_match_edit'),

               # User Auth
               url(r'^(?P<regional_code>\w+)/show_login$', show_login, name='show_login'),
               url(r'^(?P<regional_code>\w+)/log_user_out$', log_user_out, name='log_user_out'),
               url(r'^(?P<regional_code>\w+)/auth_login$', auth_login, name='auth_login'),

               ]
