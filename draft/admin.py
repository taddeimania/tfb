from django.contrib import admin
from tfb.draft.models import Draft, DraftTeam, DraftOrder, DraftPick

class DraftOrderAdmin(admin.ModelAdmin):
    list_display = ['draft_team','position']
    search_fields = ['draft_team']

class DraftPickAdmin(admin.ModelAdmin):
    list_display = ['draft_team','round', 'player']
    search_fields = ['draft_team', 'player']
    list_filter = ('round','draft_team')

admin.site.register(Draft)
admin.site.register(DraftTeam)
admin.site.register(DraftOrder, DraftOrderAdmin)
admin.site.register(DraftPick, DraftPickAdmin)
