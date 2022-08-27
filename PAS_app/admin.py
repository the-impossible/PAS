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
)

# Register your models here.
admin.site.register(Session)
admin.site.register(Programme)
admin.site.register(Department)

admin.site.register(StudentType)
admin.site.register(SupervisorRank)

admin.site.register(Files)
admin.site.register(SupervisorsFiles)