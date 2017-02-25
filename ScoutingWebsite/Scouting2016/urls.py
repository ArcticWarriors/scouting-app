'''
Created on Oct 9, 2015

@author: PJ
'''
from django.conf.urls import url
from django.views.generic.base import TemplateView, RedirectView
# from Scouting2016 import views
# from Scouting2016.view.gen_graph import gen_graph
# from Scouting2016.view.generic_views import SingleTeamView
import Scouting2016.view.match_forms as match_forms
import Scouting2016.view.pit_scouting as pit_scouting
import Scouting2016.view.user_auth as user_auth
import Scouting2016.view.standard_views as standard_views
# import views as views



app_name = 'Scouting2016'
urlpatterns = [
    
               url(r'^$', RedirectView.as_view(url='/2016/NYRO', permanent=False)),
    
               url(r'^(?P<regional_code>\w+)$', standard_views.HomepageView2016.as_view(), name='index'),

               # Add match form
               url(r'^(?P<regional_code>\w+)/form$', match_forms.show_add_form, name='match_entry'),
               url(r'^(?P<regional_code>\w+)/edit_form$', match_forms.show_edit_form, name='show_edit_form'),
               url(r'^(?P<regional_code>\w+)/pre_edit_form$', match_forms.info_for_form_edit, name='info_for_form_edit'),
               url(r'^(?P<regional_code>\w+)/submit_form$', match_forms.submit_new_match, name='show_add_form'),
               url(r'^(?P<regional_code>\w+)/submit_edit$', match_forms.edit_prev_match, name='edit_form'),

               # Pit Form
               url(r'^(?P<regional_code>\w+)/pre_pit_form$', pit_scouting.info_for_pit_edit, name='info_for_pit_edit'),
               url(r'^(?P<regional_code>\w+)/pit_form$', pit_scouting.show_add_pit, name='show_add_pit'),
               url(r'^(?P<regional_code>\w+)/submit_pit$', pit_scouting.submit_new_pit, name='submit_new_pit'),

               # User Auth
               url(r'^(?P<regional_code>\w+)/showLogin/$', user_auth.showLogin, name='showLogin'),
               url(r'^(?P<regional_code>\w+)/log_user_out$', user_auth.log_user_out, name='log_user_out'),
               url(r'^(?P<regional_code>\w+)/auth_login$', user_auth.auth_login, name='auth_login'),

               # 2016 Views
               url(r'^(?P<regional_code>\w+)/gen_graph/(?P<team_numbers>\w+(,\w+)*)/(?P<fields>\w+(,\w+)*)$', standard_views.GenGraphView2016.as_view(), name='gen_graph'),
               url(r'^(?P<regional_code>\w+)/teams$', standard_views.TeamListView2016.as_view(), name='teams'),
               url(r'^(?P<regional_code>\w+)/teams/(?P<team_number>[0-9]+)$', standard_views.SingleTeamView2016.as_view(), name='view_team'),
               url(r'^(?P<regional_code>\w+)/matches$', standard_views.MatchListView2016.as_view(), name='matches'),
               url(r'^(?P<regional_code>\w+)/matches/(?P<match_number>[0-9]+)$', standard_views.SingleMatchView2016.as_view(), name='view_match'),
               url(r'^(?P<regional_code>\w+)/match_prediction/(?P<match_number>[0-9]+)$', standard_views.OfficialMatchView2016.as_view(), name='match_prediction'),
               url(r'^(?P<regional_code>\w+)/upload_image$', standard_views.AddTeamPictureView2016.as_view(), name='upload_image'),
               url(r'^(?P<regional_code>\w+)/add_team_comments/(?P<team_number>[0-9]+)$', standard_views.AddTeamCommentsView2016.as_view(), name='add_team_comments'),

               # Robot Info
               url(r'^(?P<regional_code>\w+)/robot_display$', TemplateView.as_view(template_name='Scouting2016/robot_info/overview.html'), name='robot_display'),
               url(r'^(?P<regional_code>\w+)/robot_display/software$', TemplateView.as_view(template_name='Scouting2016/robot_info/software.html'), name='robot_display_software'),
               url(r'^(?P<regional_code>\w+)/robot_display/scaling$', TemplateView.as_view(template_name='Scouting2016/robot_info/scaling.html'), name='robot_display_scaling'),
               url(r'^(?P<regional_code>\w+)/robot_display/overroller$', TemplateView.as_view(template_name='Scouting2016/robot_info/overroller.html'), name='robot_display_overroller'),
               url(r'^(?P<regional_code>\w+)/robot_display/drivetrain$', TemplateView.as_view(template_name='Scouting2016/robot_info/drivetrain.html'), name='robot_display_drivetrain'),

               # Normal Pages
               ]
