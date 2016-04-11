'''
Created on Mar 30, 2016

@author: PJ
'''
import os
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from Scouting2011.model.reusable_models import Team, TeamPictures


def upload_image(request):

    """
    Pictures can be uploaded from the users devices to the server and posts them to the team's
    respective team page
    """

    team_numer = request.POST['team_number']
    f = request.FILES['image_name']

    static_dir = 'ScoutingWebsite2015/Scouting2011/static/'
    out_file_name = static_dir + 'Scouting2011/robot_pics/%s_{0}%s' % (team_numer, os.path.splitext(f.name)[1])

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

    team = Team.objects.get(teamNumber=team_numer)
    TeamPictures.objects.create(team=team, path=out_file_name[len(static_dir):])

    # Write the file to disk
    with open(out_file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return HttpResponseRedirect(reverse('Scouting2011:view_team', args=(team_numer,)))
