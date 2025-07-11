from django.contrib import admin
from .models import AdminPanelLoginHistory

# Register your models here.

@admin.register(AdminPanelLoginHistory)
class AdminPanelLoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_time', 'ip', 'user_agent', 'is_logged_in', 'action')
