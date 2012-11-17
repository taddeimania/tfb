from django.contrib import admin
from tfb.tecmo_player import models as tecmo_player_models

class ScheduleAdmin(admin.ModelAdmin):
    search_fields = ['home','away']
    list_filter = ('week',)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['player_name','pos', 'pro_team']
    search_fields = ['player_name']
    list_filter = ('pro_team',)

class StatsAdmin(admin.ModelAdmin):
    list_display = ['player','week', 'fanpts', 'health']
    search_fields = ['player']
    list_filter = ('week',)

admin.site.register(tecmo_player_models.Stats, StatsAdmin)
admin.site.register(tecmo_player_models.Pro_Team)
admin.site.register(tecmo_player_models.Player, PlayerAdmin)
admin.site.register(tecmo_player_models.Schedule, ScheduleAdmin)