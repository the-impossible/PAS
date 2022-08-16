# My Django imports
from django.urls import path

# My App imports
from PAS_auth.views import (
    LoginView,
    LogoutView,

    ResetPasswordView,
    DashboardView,

    # FilesView(Students)
    StudentFilesView,
    UploadStudentFilesView,
    ListFilesView,
    DeleteStudentFilesView,

    # FilesView(Supervisors)
    SupervisorFilesView,
    UploadSupervisorFilesView,
    ListSupervisorFilesView,
    DeleteSupervisorFilesView,

    # Manage Students
    ManageStudentsView,
    ManageProfile,
)

app_name = 'auth'

urlpatterns = [
    # Authentication
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('reset_password', ResetPasswordView.as_view(), name='reset_password'),

    # Dashboard
    path('dashboard', DashboardView.as_view(), name='dashboard'),

    # Files(Students)
    path('files_stud', StudentFilesView.as_view(), name='files_stud'),
    path('stud-upload-form', UploadStudentFilesView.as_view(), name='stud-upload-form'),
    path('list_student_files/<programme_id>', ListFilesView.as_view(), name='list_student_files'),
    path('delete_stud_files/<pk>', DeleteStudentFilesView.as_view(), name='delete_stud_files'),

    # # Files(Supervisors)
    path('files_super', SupervisorFilesView.as_view(), name='files_super'),
    path('super-upload-form', UploadSupervisorFilesView.as_view(), name='super-upload-form'),
    path('list_super_files', ListSupervisorFilesView.as_view(), name='list_super_files'),
    path('delete_super_files/<pk>', DeleteSupervisorFilesView.as_view(), name='delete_super_files'),

    # Manage Students
    path('manage_students', ManageStudentsView.as_view(), name='manage_students'),
    path('manage_profile', ManageProfile.as_view(), name='manage_profile'),
]
