from django.contrib import admin

# Register your models here.
from PAS_hallAllocation.models import (
    Venue,
    DaysOfDefense,
    StudHallAllocation,
    AssessorHallAllocation,
)

class StudHallAllocationAdmin(admin.ModelAdmin):
    list_display = ('stud_id', 'venue_id', 'day_num', 'sess_id', 'dept_id', 'prog_id', 'type_id',)
    search_fields = ('stud_id__user_id__username','type_id__type_title', 'dept_id__dept_title','prog_id__programme_title', 'venue_id__venue_title',)
    ordering = ('stud_id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class AssessorHallAllocationAdmin(admin.ModelAdmin):
    list_display = ('chief_assessor', 'assessor_one', 'assessor_two', 'venue_id', 'dept_id', 'prog_id', 'type_id', 'sess_id')
    search_fields = ('chief_assessor__user_id__username', 'assessor_one__user_id__username', 'assessor_two__user_id__username', 'type_id__type_title', 'dept_id__dept_title','prog_id__programme_title', 'venue_id__venue_title',)

    ordering = ('chief_assessor',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Register your models here.
admin.site.register(Venue)
admin.site.register(DaysOfDefense)
admin.site.register(StudHallAllocation, StudHallAllocationAdmin)
admin.site.register(AssessorHallAllocation, AssessorHallAllocationAdmin)
