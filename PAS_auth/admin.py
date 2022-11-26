# My Django import
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# My App import
from PAS_auth.models import User
from PAS_auth.models import StudentProfile, SupervisorProfile, Coordinators, Groups, EmailSendCount
# Register your models here.

class UserAdmin(UserAdmin):
    list_display = ('username', 'name', 'email', 'pic', 'phone', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser', 'is_super', 'is_verified' )
    search_fields = ('username','name','email',)
    ordering = ('username',)
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'programme_id', 'session_id', 'type_id', 'dept_id')
    search_fields = ('user_id__username','programme_id__programme_title','session_id__session_title','type_id__type_title', 'dept_id__dept_title')
    ordering = ('programme_id',)
    readonly_fields = ('stud_id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class SupervisorProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'rank_id', 'dept_id', 'prog_id', 'title', 'RG_capacity', 'Ev_capacity', 'super_nd')
    search_fields = ('user_id__username', 'rank_id__rank_number','title__title_description','prog_id__programme_title', 'RG_capacity')
    ordering = ('rank_id', 'dept_id')
    readonly_fields = ('super_id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class CoordinatorsAdmin(admin.ModelAdmin):
    list_display = ('chief_coord_id', 'asst_coord_id', 'dept_id', 'prog_id')
    search_fields = ('chief_coord_id','asst_coord_id','dept_id','prog_id')
    ordering = ('dept_id', 'prog_id')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, UserAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(SupervisorProfile, SupervisorProfileAdmin)
admin.site.register(Coordinators)
admin.site.register(Groups)
admin.site.register(EmailSendCount)
