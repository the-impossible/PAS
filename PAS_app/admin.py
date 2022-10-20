from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from PAS_app.models import (
    Session,
    Programme,
    StudentType,
    Files,
    SupervisorRank,
    SupervisorsFiles,
    Department,
    Title,
)

from PAS_auth.models import (
    Allocate,
)

class AllocateAdmin(UserAdmin):
    list_display = ('stud_id', 'group_id', 'prog_id', 'dept_id', 'type_id', 'super_id', 'sess_id' )
    search_fields = ('stud_id', 'super_id')
    ordering = ('prog_id', 'stud_id', 'sess_id')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Register your models here.
admin.site.register(Session)
admin.site.register(Programme)
admin.site.register(Department)

admin.site.register(StudentType)
admin.site.register(SupervisorRank)

admin.site.register(Files)
admin.site.register(SupervisorsFiles)
admin.site.register(Allocate, AllocateAdmin)
admin.site.register(Title)