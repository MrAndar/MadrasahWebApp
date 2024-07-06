from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, ClassName


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')


class ClassNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'book', 'created_at')
    list_filter = ('book', 'teacher')
    search_fields = ('name', 'teacher__user__first_name', 'teacher__user__last_name')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(ClassName, ClassNameAdmin)
