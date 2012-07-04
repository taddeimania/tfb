from django.contrib import admin
from tfb.messages.models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'message']

admin.site.register(Message, MessageAdmin)
