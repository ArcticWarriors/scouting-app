from BaseScouting.views.base_views import BaseAddTeamPictureView
from Scouting2016.model.reusable_models import Team, TeamPictures


class AddTeamPictureView2016(BaseAddTeamPictureView):

    def __init__(self):
        BaseAddTeamPictureView.__init__(self, Team, TeamPictures, 'Scouting2016/static', 'Scouting2016/robot_pics', 'Scouting2016:view_team')
