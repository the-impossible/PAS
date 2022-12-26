from django.urls import path

# My app imports
from PAS_assessment.views import (
    WhatAssessmentView,
    CRSeminarAssessmentView,
    ProgrammeTypeSelectionView,
    CRSuperAssessorSeminarAssessmentView,
)

app_name = 'assess'

urlpatterns = [
    path('what_assess/<str:dept_id>', WhatAssessmentView.as_view(), name='what_assess'),
    path('assess_seminar/<str:dept_id>', CRSeminarAssessmentView.as_view(), name='assess_seminar'),
    path('super_assess_seminar/<str:dept_id>/<str:type_id>/<str:prog_id>/<str:sess_id>', CRSuperAssessorSeminarAssessmentView.as_view(), name='super_assess_seminar'),
    path('programme_selection/<str:dept_id>', ProgrammeTypeSelectionView.as_view(), name='programme_selection'),
]