# My Django imports
from django.urls import path

# My App imports
from PAS_hallAllocation.views import (
    HallAllocationDashboardView,
    # Venues
    VenuesView,
    UDVenuesView,
    # Defense
    DefenseDaysView,
    UDDefenseDaysView,
    # Hall Allocation
    CRStudentHallAllocationView,
    ManageHallAllocationView,
    CRAssessorHallAllocationView,
    # Check Allocation
    CheckHallAllocationView,
    CheckAssessmentHallView,
)

app_name = 'hall'

urlpatterns = [
    path('dashboard/<str:dept_id>', HallAllocationDashboardView.as_view(), name='dashboard'),
    # VENUES
    path('venues/<str:dept_id>', VenuesView.as_view(), name='venues'),
    path('edit_venue/<str:dept_id>/<str:venue_id>', UDVenuesView.as_view(), name='UD_venue'),
    # DEFENSES_DAYS
    path('defense_days/<str:dept_id>', DefenseDaysView.as_view(), name='defense_days'),
    path('UD_defense_id/<str:dept_id>/<str:day_id>', UDDefenseDaysView.as_view(), name='UD_defense_id'),
    # HALL_ALLOCATION
    path('cr_student_hall/<str:dept_id>', CRStudentHallAllocationView.as_view(), name='cr_student_hall'),
    path('manage_hall_allocation/<str:dept_id>', ManageHallAllocationView.as_view(),name='manage_hall_allocation'),

    path('cr_assessor_hall/<str:dept_id>', CRAssessorHallAllocationView.as_view(), name='cr_assessor_hall'),
    # Check Allocation
    path('view_venue', CheckHallAllocationView.as_view(), name='view_venue'),
    path('view_assessment_hall', CheckAssessmentHallView.as_view(), name='view_assessment_hall'),

]