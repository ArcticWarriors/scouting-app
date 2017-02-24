'''
Created on Jan 15, 2017

@author: PJ
'''
from django.conf.urls import url
from django.views.generic.base import RedirectView
from Scouting2017.view import standard_views, match_forms
from Scouting2017.view import user_auth
from django.contrib.auth.decorators import permission_required


app_name = 'Scouting2017'
urlpatterns = [
    
               url(r'^$', RedirectView.as_view(url='/2017/NYRO', permanent=False)),
               url(r'^(?P<regional_code>\w+)$', standard_views.HomepageView2017.as_view(), name='index'),
               url(r'^(?P<regional_code>\w+)/teams$', standard_views.TeamListView2017.as_view(), name='teams'),
               url(r'^(?P<regional_code>\w+)/matches$', standard_views.MatchListView2017.as_view(), name='matches'),
               url(r'^(?P<regional_code>\w+)/matches/(?P<match_number>[0-9]+)$', standard_views.SingleMatchView2017.as_view(), name='view_match'),
               url(r'^(?P<regional_code>\w+)/teams/(?P<team_number>[0-9]+)$', standard_views.SingleTeamView2017.as_view(), name='view_team'),
               # url(r'^(?P<regional_code>\w+)/pick_list$', standard_views.PickListView2017.as_view(), name='pick_list'),
               
               # Forms
               url(r'^(?P<regional_code>\w+)/match_entry$', match_forms.MatchEntryView2017.as_view(), name='match_entry'),
               url(r'^(?P<regional_code>\w+)/submit_new_match$', match_forms.add_match, name='submit_new_match'),
               
               # User Auth
               url(r'^(?P<regional_code>\w+)/show_login/$', user_auth.show_login, name='show_login'),
               url(r'^(?P<regional_code>\w+)/log_user_out$', user_auth.log_user_out, name='log_user_out'),
               url(r'^(?P<regional_code>\w+)/auth_login$', user_auth.auth_login, name='auth_login'),
               ]