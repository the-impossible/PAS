# My Django import
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# My App import
from PAS_auth.models import User
# Register your models here.

class UserAdmin(UserAdmin):
    list_display = ('username', 'firstname', 'lastname', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser' )
    search_fields = ('username',)
    ordering = ('username',)
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, UserAdmin)