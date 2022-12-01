# My Django imports
from django.urls import path

# My App imports
from PAS_hallAllocation.views import (
    HallAllocationDashboardView,
    VenuesView,
    EditVenuesView,
    DeleteVenuesView,
)

app_name = 'hall'

urlpatterns = [
    path('dashboard/<str:dept_id>', HallAllocationDashboardView.as_view(), name='dashboard'),
    # VENUES
    path('venues/<str:dept_id>', VenuesView.as_view(), name='venues'),
    path('edit_venue/<str:dept_id>/<str:venue_id>', EditVenuesView.as_view(), name='edit_venue'),
    path('delete_venue/<str:dept_id>/<str:venue_id>', DeleteVenuesView.as_view(), name='delete_venue'),
]