from django.contrib import admin
from app.models import Resource

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
  list_display = ('name', 'created_at')
  list_filter = ('name', 'created_at')
