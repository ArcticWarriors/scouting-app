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
urlpatterns = [
                 url(r'^$', TemplateView.as_view(template_name="Scouting2016/index.html"), name='index'),

                # Add match form
                url(r'^form$', match_forms.show_add_form, name='showForm'),
                url(r'^edit_form$', match_forms.show_edit_form, name='show_edit_form'),
                url(r'^pre_edit_form$', match_forms.info_for_form_edit, name='info_for_form_edit'),
                url(r'^submit_form$', match_forms.submit_new_match, name='show_add_form'),
                url(r'^submit_edit$', match_forms.edit_prev_match, name='edit_form'),

                # Pit Form
                url(r'^pre_pit_form$', pit_scouting.info_for_pit_edit, name='info_for_pit_edit'),
                url(r'^pit_form$', pit_scouting.show_add_pit, name='show_add_pit'),
                url(r'^submit_pit$', pit_scouting.submit_new_pit, name='submit_new_pit'),

                # User Auth
                url(r'^showLogin/$', user_auth.showLogin, name='showLogin'),
                url(r'^log_user_out$', user_auth.log_user_out, name='log_user_out'),
                url(r'^auth_login$', user_auth.auth_login, name='auth_login'),

                # Generic Views
                url(r'^gen_graph/(?P<team_numbers>\w+(,\w+)*)/(?P<fields>\w+(,\w+)*)$', gen_graph.gen_graph, name='gen_graph'),
                url(r'^upload_image$', generic_views.upload_image, name='upload_image'),
                url(r'^teams$', generic_views.all_teams, name='teams'),
                url(r'^matches$', generic_views.all_matches, name='matches'),
                url(r'^matches/(?P<match_number>[0-9]+)$', generic_views.match_display, name='all_matches'),
                url(r'^add_team_comments/(?P<team_number>[0-9]+)$', generic_views.add_team_comments, name='add_team_comments'),

                # Robot Info
                url(r'^robot_display$', TemplateView.as_view(template_name='Scouting2016/robot_info/overview.html'), name='robot_display'),
                url(r'^robot_display/software$', TemplateView.as_view(template_name='Scouting2016/robot_info/software.html'), name='robot_display_software'),
                url(r'^robot_display/scaling$', TemplateView.as_view(template_name='Scouting2016/robot_info/scaling.html'), name='robot_display_scaling'),
                url(r'^robot_display/overroller$', TemplateView.as_view(template_name='Scouting2016/robot_info/overroller.html'), name='robot_display_overroller'),
                url(r'^robot_display/drivetrain$', TemplateView.as_view(template_name='Scouting2016/robot_info/drivetrain.html'), name='robot_display_drivetrain'),


                url(r'^bookmark_team_page$', views.bookmark_team_page, name='bookmark'),

                # Normal Pages
                url(r'^teams/(?P<team_number>[0-9]+)$', generic_views.SingleTeamView.as_view(), name='view_team'),
                url(r'^search$', views.search_page, name='search_page'),
                url(r'^graph$', views.show_graph, name='show_graph'),
                url(r'^match_prediction/(?P<match_number>[0-9]+)$', views.match_prediction, name='match_prediction'),
                url(r'^hovercards$', views.get_hovercard, name='hovercards'),
               ]
