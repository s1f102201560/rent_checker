from django.contrib import admin
from app.models import Resource, ChatLog

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
  list_display = ('name', 'created_at')
  list_filter = ('name', 'created_at')
  exclude = ('embedding',)

@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'prompt', 'response')
    list_filter = ('created_at',)

