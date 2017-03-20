from BaseScouting.views.submissions.submit_team_picture import BaseAddTeamPictureView
from Scouting2017.model.reusable_models import Team, TeamPictures


class AddTeamPictureView2017(BaseAddTeamPictureView):

    def __init__(self):
        BaseAddTeamPictureView.__init__(self, Team, TeamPictures, 'Scouting2017/static', 'Scouting2017/robot_pics', 'Scouting2017:view_team')
