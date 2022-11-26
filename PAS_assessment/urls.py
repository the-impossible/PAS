from django.urls import path

# My app imports
from PAS_assessment.views import (
    WhatAssessmentView,
)

app_name = 'assess'

urlpatterns = [
    path('what_assess/<str:dept_id>', WhatAssessmentView.as_view(), name='what_assess'),
]