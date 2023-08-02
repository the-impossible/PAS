from django.contrib import admin

from PAS_assessment.models import (
    Assessment,
    SeminarAssessment,
    ProjectAssessment,
)

# Register your models here.

class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'assessor_id', 'supervisor','seminar_defense_grade', 'project_defense_grade', 'supervisor_grade', 'prog_id', 'sess_id', 'type_id', 'dept_id',)
    search_fields = ('student_id__stud_id__user_id__username','student_id__stud_id__user_id__name','assessor_id__user_id__username', 'assessor_id__user_id__name','type_id__type_title', 'dept_id__dept_title','prog_id__programme_title',)
    ordering = ('student_id__stud_id__user_id__username',)
    raw_id_fields = ['student_id', 'assessor_id', 'supervisor']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(SeminarAssessment)
admin.site.register(ProjectAssessment)