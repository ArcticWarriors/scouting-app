from BaseScouting.views.base_views import BaseAddTeamPictureView
from Scouting2013.model.reusable_models import Team, TeamPictures

class AddTeamPictureView2013(BaseAddTeamPictureView):

    def __init__(self):
        BaseAddTeamPictureView.__init__(self, Team, TeamPictures, 'Scouting2013/static', 'Scouting2013/robot_pics', 'Scouting2013:view_team')