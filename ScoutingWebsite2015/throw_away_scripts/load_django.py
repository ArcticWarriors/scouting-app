'''
Created on Mar 9, 2016

@author: PJ
'''
import os
import sys
from django.core.wsgi import get_wsgi_application


def load_django():
    os.environ["DJANGO_SETTINGS_MODULE"] = "ScoutingWebsite.settings"
    proj_path = os.path.abspath("..")
    sys.path.append(proj_path)
    _ = get_wsgi_application()
