from django.contrib import admin
from tfb.players import models as player_models

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name','league', 'iscommish']
    list_filter = ('league',)

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

class RosterAdmin(admin.ModelAdmin):
    list_display = ['team','week', 'player']
    search_fields = ['player', 'team']
    list_filter = ('team',)

class TrophyAssignmentAdmin(admin.ModelAdmin):
    list_display = ['trophy', 'profile', 'season']

admin.site.register(player_models.SeasonRanking)
admin.site.register(player_models.UserProfile, UserProfileAdmin)
admin.site.register(player_models.Season)
admin.site.register(player_models.Curweek)
admin.site.register(player_models.Trophy)
admin.site.register(player_models.TrophyAssignment, TrophyAssignmentAdmin)
admin.site.register(player_models.Roster, RosterAdmin)
admin.site.register(player_models.Stats, StatsAdmin)
admin.site.register(player_models.Pro_Team)
admin.site.register(player_models.Player, PlayerAdmin)
admin.site.register(player_models.Schedule, ScheduleAdmin)
admin.site.register(player_models.League)
admin.site.register(player_models.Team, TeamAdmin)