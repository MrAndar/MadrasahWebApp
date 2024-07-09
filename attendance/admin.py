from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('profile__user__first_name', 'profile__user__username', 'date')
