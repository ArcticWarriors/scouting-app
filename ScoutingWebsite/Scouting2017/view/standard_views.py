from BaseScouting.views.base_views import BaseHomepageView, BaseAllTeamsViews,\
    BaseAllMatchesView
from Scouting2017.model.reusable_models import Competition



class HomepageView2017(BaseHomepageView):
 
    def __init__(self):
        BaseHomepageView.__init__(self, Competition, 'Scouting2017/index.html')
 
    def get_our_metrics(self):
 
        return []
 
    def get_competition_metrics(self, competition):
 
        output = []
 
        return output

class AllTeamsViews2017(BaseAllTeamsViews):
    pass
class AllMatchesViews2017(BaseAllMatchesView):
    pass