from BaseScouting.views.base_views import BaseHomepageView
from Scouting2017.model.reusable_models import Competition


class HomepageView2017(BaseHomepageView):

    def __init__(self):
        BaseHomepageView.__init__(self, Competition, 'BaseScouting/index.html')

    def get_our_metrics(self):

        return []

    def get_competition_metrics(self, competition):

        output = []

        return output
