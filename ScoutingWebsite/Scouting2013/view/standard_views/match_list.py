from Scouting2013.model.reusable_models import Match, OfficialMatch
from BaseScouting.views.base_views import BaseMatchListView


class AllMatchesView2013(BaseMatchListView):

    def __init__(self):
        BaseMatchListView.__init__(self, Match, OfficialMatch, 'Scouting2013/all_matches.html')