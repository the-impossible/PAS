from django.urls import path

# My app imports
from PAS_assessment.views import (
    WhatAssessmentView,
    CRSeminarAssessmentView,
    CRSuperAssessorSeminarAssessmentView,

    CRProjectAssessmentView,
    CRSuperAssessorProjectAssessmentView,
    UDProjectAssessmentView,

    ProgrammeTypeSelectionView,

    UDSeminarAssessmentView,
    UDSuperAssessorProjectAssessmentView,
    UDSuperAssessorSeminarAssessmentView,

    GradeStudentView,
    UDGradeStudentView,

    CRSuperSupervisorAssessmentView,
    UDSuperAssessorProjectAssessmentView,
)

app_name = 'assess'

urlpatterns = [
    path('what_assess/<str:dept_id>', WhatAssessmentView.as_view(), name='what_assess'),
    # SEMINAR
    path('assess_seminar/<str:dept_id>', CRSeminarAssessmentView.as_view(), name='assess_seminar'),

    path('super_assess_seminar/<str:dept_id>/<str:type_id>/<str:prog_id>/<str:sess_id>', CRSuperAssessorSeminarAssessmentView.as_view(), name='super_assess_seminar'),

    # PROJECT
    path('assess_project/<str:dept_id>', CRProjectAssessmentView.as_view(), name='assess_project'),
    path('super_assess_project/<str:dept_id>/<str:type_id>/<str:prog_id>/<str:sess_id>', CRSuperAssessorProjectAssessmentView.as_view(), name='super_assess_project'),

    path('ud_super_assess_project/<str:dept_id>/<str:prog_id>/<str:type_id>/<str:sess_id>/<str:assess_id>', UDSuperAssessorProjectAssessmentView.as_view(), name='ud_super_assess_project'),

    path('super_assess_supervisor/<str:dept_id>/<str:type_id>/<str:prog_id>/<str:sess_id>', CRSuperSupervisorAssessmentView.as_view(), name='super_assess_supervisor'),

    path('ud_assess_project/<str:dept_id>/<str:assess_id>', UDProjectAssessmentView.as_view(), name='ud_assess_project'),

    path('programme_selection/<str:dept_id>/<str:grade_type>', ProgrammeTypeSelectionView.as_view(), name='programme_selection'),

    path('ud_assess_seminar/<str:dept_id>/<str:assess_id>', UDSeminarAssessmentView.as_view(), name='ud_assess_seminar'),

    path('ud_super_assess_seminar/<str:dept_id>/<str:prog_id>/<str:type_id>/<str:sess_id>/<str:assess_id>', UDSuperAssessorSeminarAssessmentView.as_view(), name='ud_super_assess_seminar'),
    path('ud_super_assess_project/<str:dept_id>/<str:prog_id>/<str:type_id>/<str:sess_id>/<str:assess_id>', UDSuperAssessorProjectAssessmentView.as_view(), name='ud_super_assess_project'),

    path('grade_student', GradeStudentView.as_view(), name='grade_student'),
    path('ud_grade_student/<str:assess_id>/<str:type_id>', UDGradeStudentView.as_view(), name='ud_grade_student'),


]