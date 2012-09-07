from django.contrib import admin
from tfb.matchup.models import Matchup

class MatchupAdmin(admin.ModelAdmin):
    list_display = ['week', 'team_one', 'team_two']
    search_fields = ['player', 'team']
    list_filter = ('league',)

admin.site.register(Matchup, MatchupAdmin)