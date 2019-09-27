from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class NewUserAdmin(UserAdmin):
    model = User
    fieldsets = [(None, {'fields': ('username', 'password', 'email')})]


admin.site.register(User, NewUserAdmin)
