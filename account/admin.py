from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
@admin.register(User)
class UserModelAdmin(BaseUserAdmin):
    list_display = ['id', 'email', 'name', 'is_admin']
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials',{'fields': ('email', 'password')}),
        ('Personal info', {'fields':('name',)}),
        ('Permission', {'fields':('is_admin',)}),
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields': ('email', 'name', 'password1', 'password2')
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()

