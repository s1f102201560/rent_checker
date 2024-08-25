from django.contrib import admin
from registration.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ('username', 'name', 'email', 'phone_number', 'created')
  search_fields = ('username', 'name', 'email')
  list_filter = ('created', 'updated_at')
  ordering = ('-created',)

  fieldsets = (
      (None, {
          'fields': ('username', 'password')
      }),
      ('Personal info', {
          'fields': ('name', 'email', 'phone_number', 'address')
      }),
      ('Important dates', {
          'fields': ('last_login', 'created', 'updated_at')
      }),
  )
  readonly_fields = ('created', 'updated_at', 'last_login')