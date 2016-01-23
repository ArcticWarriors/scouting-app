'''
Created on Oct 9, 2015

@author: PJ
'''
from django.conf.urls import url
from . import views


app_name = 'Scouting2016'
urlpatterns = [
               url(r'^$', views.index, name='index'),
               url(r'^form$', views.showForm, name='showForm'),
               url(r'^submit_form$', views.submitForm, name='submit_form'),
              ]
