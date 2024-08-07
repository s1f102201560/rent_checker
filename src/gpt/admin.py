from django.contrib import admin
from .models import Memo

# デバック用(本番環境では使用しない予定)
admin.site.register(Memo)
