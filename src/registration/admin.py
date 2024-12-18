from django.contrib import admin
from registration.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ('username', 'name', 'email', 'phone_number', 'created_at')
  search_fields = ('username', 'name', 'email')
  list_filter = ('created_at', 'updated_at')
  ordering = ('-created_at',)

  fieldsets = (
      (None, {
          'fields': ('username', 'password')
      }),
      ('Personal info', {
          'fields': ('name', 'email', 'phone_number', 'address')
      }),
      ('Important dates', {
          'fields': ('last_login', 'created_at', 'updated_at')
      }),
  )
  readonly_fields = ('created_at', 'updated_at', 'last_login')