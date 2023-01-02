from django.contrib import admin

# Register your models here.
from PAS_hallAllocation.models import (
    Venue,
    DaysOfDefense,
    StudHallAllocation,
    AssessorHallAllocation,
)

# Register your models here.
admin.site.register(Venue)
admin.site.register(DaysOfDefense)
admin.site.register(StudHallAllocation)
admin.site.register(AssessorHallAllocation)