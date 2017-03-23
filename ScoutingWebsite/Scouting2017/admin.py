from django.contrib import admin

# Register your models here.
from Scouting2017.model.reusable_models import Team, TeamComments, TeamPictures
from Scouting2017.model.models2017 import ScoreResult, Scout

admin.site.register(Team)
admin.site.register(Scout)
admin.site.register(ScoreResult)
admin.site.register(TeamComments)
admin.site.register(TeamPictures)
