'''
Created on Jan 15, 2017

@author: PJ
'''
from django.conf.urls import url
from django.views.generic.base import RedirectView
from Scouting2017.view import standard_views


app_name = 'Scouting2017'
urlpatterns = [
    
               url(r'^$', RedirectView.as_view(url='/2017/NYRO', permanent=False)),
               url(r'^(?P<regional_code>\w+)$', standard_views.HomepageView2017.as_view(), name='index'),
               
               ]