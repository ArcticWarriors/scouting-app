'''
Created on Oct 9, 2015

@author: PJ
'''
from django.conf.urls import url
from Scouting2016 import views
import view.generic_views as generic_views
import view.user_auth as user_auth


app_name = 'Scouting2016'
urlpatterns = [url(r'^$', generic_views.index, name='index'),

               # Add/Edit Form
               url(r'^form$', views.show_add_form, name='showForm'),

               url(r'^edit_form$', views.show_edit_form, name='show_edit_form'),
               url(r'^pre_edit_form$', views.info_for_form_edit, name='info_for_form_edit'),
               url(r'^submit_form$', views.submit_new_match, name='show_add_form'),

               url(r'^submit_edit$', views.edit_prev_match, name='edit_form'),

               # User Auth
               url(r'^showLogin/$', user_auth.showLogin, name='showLogin'),
               url(r'^log_user_out$', user_auth.log_user_out, name='log_user_out'),
               url(r'^auth_login$', user_auth.auth_login, name='auth_login'),

               # Generic Views
               url(r'^robot_display$', generic_views.robot_display, name='robot_display'),
               url(r'^match_display/(?P<match_number>[0-9]+)$', generic_views.match_display, name='match_display'),
               url(r'^gen_graph/(?P<team_numbers>\w+(,\w+)*)/(?P<fields>\w+(,\w+)*)$', generic_views.gen_graph, name='gen_graph'),
               url(r'^upload_image$', generic_views.upload_image, name='upload_image'),
               url(r'^all_teams$', generic_views.all_teams, name='all_teams'),
               url(r'^all_matches$', generic_views.all_matches, name='all_matches'),
               url(r'^add_team_comments/(?P<team_number>[0-9]+)$', generic_views.add_team_comments, name='add_team_comments'),

               # Robot Info
               url(r'^robot_display/software$', views.robot_display_software, name='robot_display_software'),
               url(r'^robot_display/scaling$', views.robot_display_scaling, name='robot_display_scaling'),
               url(r'^robot_display/overroller$', views.robot_display_overroller, name='robot_display_overroller'),
               url(r'^robot_display/drivetrain$', views.robot_display_drivetrain, name='robot_display_drivetrain'),


               url(r'^bookmark_team_page$', views.bookmark_team_page, name='bookmark'),

               # Pit Form
               url(r'^pre_pit_form$', views.info_for_pit_edit, name='info_for_pit_edit'),
               url(r'^pit_form$', views.show_add_pit, name='show_add_pit'),
               url(r'^submit_pit$', views.submit_new_pit, name='submit_new_pit'),

               # Normal Pages
               url(r'^view_team/(?P<team_number>[0-9]+)$', views.view_team, name='view_team'),
               url(r'^search$', views.search_page, name='search_page'),
               url(r'^graph$', views.show_graph, name='show_graph'),
               url(r'^match_prediction/(?P<match_number>[0-9]+)$', views.match_prediction, name='match_prediction'),
               url(r'^comparison$', views.show_comparison, name='comparison'),
               url(r'^hovercards$', views.get_hovercard, name='hovercards'),
               ]
