from BaseScouting.views.base_views import BaseAddTeamPictureView
from Scouting2011.model.reusable_models import Team, TeamPictures

class AddTeamPictureView2011(BaseAddTeamPictureView):

    def __init__(self):
        BaseAddTeamPictureView.__init__(self, Team, TeamPictures, 'Scouting2011/static', 'Scouting2011/robot_pics', 'Scouting2011:view_team')