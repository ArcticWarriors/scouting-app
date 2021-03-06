from django.views.generic.base import View
from django.http import HttpResponse


class BaseGenGraphView(View):

    def __init__(self, team_model):
        self.team_model = team_model

    def get(self, request, **kwargs):

        fields = kwargs['fields']
        team_numbers = kwargs['team_numbers']

        """
        @param team_numbers is the list of all checked team numbers on the show_graph page.
        @param fields is the list of all checked fields on the show_graph page
        these two parameters determine what is graphed and displayed on the page
        """

        import matplotlib
        matplotlib.use('agg')
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        from matplotlib.font_manager import FontProperties

        team_numbers = [int(x) for x in team_numbers.split(",")]
        fields = fields.split(',')

        f = plt.figure(figsize=(6, 6))
        legend_handles = []

        for team_number in team_numbers:
            team = self.team_model.objects.get(teamNumber=int(team_number))

            for field in fields:
                metric = []
                for result in team.scoreresult_set.all():
                    metric.append(getattr(result, field))

                hand, = plt.plot(metric, label="Team %s, %s" % (team.teamNumber, field))
                legend_handles.append(hand)

        fontP = FontProperties()
        fontP.set_size('small')
        plt.legend(handles=legend_handles, prop=fontP)
        plt.xlabel("Match")

        matplotlib.pyplot.close(f)
        canvas = FigureCanvasAgg(f)
        response = HttpResponse(content_type='image/png')
        canvas.print_png(response)

        return response

