'''
Created on Mar 19, 2017

@author: PJ
'''
import os
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic.base import View


class BaseAddTeamPictureView(View):

    def __init__(self, team_model, team_pictures_model, static_dir, picture_location, reverse_name):
        self.team_model = team_model
        self.team_pictures_model = team_pictures_model

        self.static_dir = static_dir
        self.picture_location = picture_location
        self.reverse_name = reverse_name

    def post(self, request, **kargs):

        """
        Pictures can be uploaded from the users devices to the server and posts them to the team's
        respective team page
        """

        regional_code = kargs['regional_code']
        team_numer = request.POST['team_number']
        f = request.FILES['image_name']

        out_file_name = os.path.join(self.static_dir, self.picture_location) + "/" + ('%s_{0}%s' % (team_numer, os.path.splitext(f.name)[1]))

        # Look for the next available number, i.e. if there are [#_0, #_1, ..., #_10], this would make the new picture #_11
        picture_number = 0
        found = False
        while not found:
            test_name = out_file_name.format(picture_number)
            if not os.path.exists(test_name):
                out_file_name = test_name
                found = True
            else:
                picture_number += 1

        database_name = out_file_name[len(self.static_dir) + 1:]

        team = self.team_model.objects.get(teamNumber=team_numer)
        self.team_pictures_model.objects.create(team=team, path=database_name)

        # Write the file to disk
        with open(out_file_name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        return HttpResponseRedirect(reverse(self.reverse_name, args=(regional_code, team_numer,)))
