'''
Created on Oct 9, 2015

@author: PJ
'''
from django.conf.urls import url
from django.views.generic.base import TemplateView
from Scouting2016 import views
# from Scouting2016.view.gen_graph import gen_graph
# from Scouting2016.view.generic_views import SingleTeamView
import view.generic_views as generic_views
import view.gen_graph as gen_graph
import view.match_forms as match_forms
import view.pit_scouting as pit_scouting
import view.user_auth as user_auth
# import views as views


app_name = 'Scouting2016'
urlpatterns = [url(r'^(?P<regional_code>\w+)$', TemplateView.as_view(template_name="Scouting2016/index.html"), name='index'),

               # Add match form
               url(r'^(?P<regional_code>\w+)/form$', match_forms.show_add_form, name='showForm'),
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

               # Generic Views
               url(r'^(?P<regional_code>\w+)/gen_graph/(?P<team_numbers>\w+(,\w+)*)/(?P<fields>\w+(,\w+)*)$', gen_graph.gen_graph, name='gen_graph'),
               url(r'^(?P<regional_code>\w+)/matches$', generic_views.AllMatchesView.as_view(), name='matches'),
               url(r'^(?P<regional_code>\w+)/add_team_comments/(?P<team_number>[0-9]+)$', generic_views.AddTeamCommentsView.as_view(), name='add_team_comments'),

               # 2016 Views
               url(r'^(?P<regional_code>\w+)/teams$', views.AllTeamsViews2016.as_view(), name='teams'),
               url(r'^(?P<regional_code>\w+)/teams/(?P<team_number>[0-9]+)$', views.SingleTeamView2016.as_view(), name='view_team'),
               url(r'^(?P<regional_code>\w+)/matches/(?P<match_number>[0-9]+)$', views.SingleMatchView2016.as_view(), name='view_match'),
               url(r'^(?P<regional_code>\w+)/match_prediction/(?P<match_number>[0-9]+)$', views.OfficialMatchView2016.as_view(), name='match_prediction'),
               url(r'^(?P<regional_code>\w+)/upload_image$', views.AddTeamPictureView2016.as_view(), name='upload_image'),

               # Robot Info
               url(r'^(?P<regional_code>\w+)/robot_display$', TemplateView.as_view(template_name='Scouting2016/robot_info/overview.html'), name='robot_display'),
               url(r'^(?P<regional_code>\w+)/robot_display/software$', TemplateView.as_view(template_name='Scouting2016/robot_info/software.html'), name='robot_display_software'),
               url(r'^(?P<regional_code>\w+)/robot_display/scaling$', TemplateView.as_view(template_name='Scouting2016/robot_info/scaling.html'), name='robot_display_scaling'),
               url(r'^(?P<regional_code>\w+)/robot_display/overroller$', TemplateView.as_view(template_name='Scouting2016/robot_info/overroller.html'), name='robot_display_overroller'),
               url(r'^(?P<regional_code>\w+)/robot_display/drivetrain$', TemplateView.as_view(template_name='Scouting2016/robot_info/drivetrain.html'), name='robot_display_drivetrain'),

               # Normal Pages
               ]
