from django.views.generic.base import TemplateView


class BaseMatchEntryView(TemplateView):
    def __init__(self, template_name):
        self.template_name = template_name

    def get_context_data(self, **kwargs):
        context = super(BaseMatchEntryView, self).get_context_data(**kwargs)

        return context
