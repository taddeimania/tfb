from django.contrib import admin
from tfb.players.models import SeasonRanking, Team, UserProfile, League, Schedule, Player, \
    Pro_Team, Stats, Roster, Curweek, Matchup, Trophy, TrophyAssignment, Season

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


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

class MatchupAdmin(admin.ModelAdmin):
    list_display = ['week', 'team_one', 'team_two']
    search_fields = ['player', 'team']
    list_filter = ('league',)

class TrophyAssignmentAdmin(admin.ModelAdmin):
    list_display = ['trophy', 'profile', 'season']

admin.site.register(SeasonRanking)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Season)
admin.site.register(Curweek)
admin.site.register(Trophy)
admin.site.register(TrophyAssignment, TrophyAssignmentAdmin)
admin.site.register(Matchup, MatchupAdmin)
admin.site.register(Roster, RosterAdmin)
admin.site.register(Stats, StatsAdmin)
admin.site.register(Pro_Team)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(League)
admin.site.register(Team, TeamAdmin)