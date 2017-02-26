'''
Created on Feb 26, 2017

@author: PJ
'''
import os
from BaseScouting.load_django import load_django

load_django()
from Scouting2017.model import TeamPictures, Team

dir_to_crawl = r'C:\Users\PJ\GitHub\SnobotScouting\scouting-app\ScoutingWebsite\Scouting2017\static\Scouting2017\robot_pics'




for f in os.listdir(dir_to_crawl):
    
    image_path = "Scouting2017/robot_pics/" + f
    
    underscore_pos = f.find("_")
    team_number = team_number = f[:underscore_pos]
    
    image_search = TeamPictures.objects.filter(path=image_path)
    if len(image_search) == 0:
        team, _ = Team.objects.get_or_create(teamNumber=team_number)
        TeamPictures.objects.create(path=image_path, team=team)

#     extension_pos = f.find(".")
#     team_number = f[:underscore_pos]
#     print team_number, image_number
    
#     print f