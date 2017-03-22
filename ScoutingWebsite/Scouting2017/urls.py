'''
Created on Jan 15, 2017

@author: PJ
'''
from django.conf.urls import url
from django.views.generic.base import RedirectView
from Scouting2017.view.forms import create_match
from Scouting2017.api_scraper.the_blue_alliance import tba_webook
from Scouting2017.view.submissions.submit_bookmark import UpdateBookmarks2017
from Scouting2017.view.submissions.submit_match_edit import SubmitMatchEdit2017
from Scouting2017.view.submissions.submit_pick_list import SubmitPickList2017
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
from Scouting2017.view.submissions.submit_team_comments import AddTeamCommentsView2017
from django.contrib.auth.decorators import permission_required
from Scouting2017.view.submissions import submit_match, submit_pit_scouting
from Scouting2017.view.standard_views.download_match_inconsistancies import download_match_inconsistancies


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
               url(r'^(?P<regional_code>\w+)/match_entry$', permission_required('Scouting2017.add_scoreresult', raise_exception=True)(create_match.MatchEntryView2017.as_view()), name='match_entry'),

               # Submission backends
               url(r'^(?P<regional_code>\w+)/submit_new_match$', permission_required('Scouting2017.add_scoreresult', raise_exception=True)(submit_match.BulkSubmitMatch.as_view()), name='submit_new_match'),
               url(r'^(?P<regional_code>\w+)/submit_pit_scouting$', permission_required('Scouting2017.add_scoreresult', raise_exception=True)(submit_pit_scouting.SubmitPitScouting.as_view()), name='submit_pit_scouting'),
               url(r'^(?P<regional_code>\w+)/upload_image$', permission_required('Scouting2017.add_teampictures', raise_exception=True)(AddTeamPictureView2017.as_view()), name='upload_image'),
               url(r'^(?P<regional_code>\w+)/update_bookmark$', UpdateBookmarks2017.as_view(), name='update_bookmark'),
               url(r'^(?P<regional_code>\w+)/submit_match_edit$', permission_required('Scouting2017.change_scoreresult', raise_exception=True)(SubmitMatchEdit2017.as_view()), name='submit_match_edit'),
               url(r'^(?P<regional_code>\w+)/submit_pick_list$', permission_required('Scouting2017.change_picklist', raise_exception=True)(SubmitPickList2017.as_view()), name='submit_pick_list'),
               url(r'^(?P<regional_code>\w+)/add_team_comments/(?P<team_number>[0-9]+)$', permission_required('Scouting2017.add_teamcomments', raise_exception=True)(AddTeamCommentsView2017.as_view()), name='add_team_comments'),

               # User Auth
               url(r'^(?P<regional_code>\w+)/login/$', show_login, name='show_login'),
               url(r'^(?P<regional_code>\w+)/log_user_out$', log_user_out, name='log_user_out'),
               url(r'^(?P<regional_code>\w+)/auth_login$', auth_login, name='auth_login'),

               url(r'^(?P<regional_code>\w+)/download_match_inconsistancies', download_match_inconsistancies, name='download_match_inconsistancies'),


               ]
