'''
Created on Oct 9, 2015

@author: PJ
'''
from django.conf.urls import url
from . import views


urlpatterns = [
               url(r'^$', views.index, name='index'),
              ]
