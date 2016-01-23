from django.contrib import admin

# Register your models here.

from models import Match, Team


admin.site.register(Match)
admin.site.register(Team)
