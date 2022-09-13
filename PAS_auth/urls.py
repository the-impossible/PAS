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
    ListDepartmentView,
    ListFilesView,
    DeleteStudentFilesView,
    ListStudentView,

    # FilesView(Supervisors)
    SupervisorFilesView,
    ListSupervisorFilesView,
    DeleteSupervisorFilesView,

    # Manage Users
    ManageStudentsView,
    DeleteUserAccountView,
    ManageSupervisorsView,
    ManageAdministratorsView,

    # Department
    DepartmentView,

    # Allocation
    AllocateView,
    ManageAllocationsView,

    ManageProfileView,
    SettingsView,
    NotificationsView,
    HelpView,
    WhatFileView,
    BatchCreateView,

    ListSupervisorView,
    ManageCoordinatorsView,
    StudentDashboardView,

    ReVerifyEmailView,
    ResendEmailVerificationView,
    EmailActivationView,
    ResetPasswordActivationView,

    AssignedStudentView,
    AssignedSupervisorView,
    DisplayGroupMembersView,

)

app_name = 'auth'

urlpatterns = [
    # Authentication
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    # Dashboard
    path('dashboard', DashboardView.as_view(), name='dashboard'),

    # Files(Students)
    path('files_stud/<str:dept_id>', StudentFilesView.as_view(), name='files_stud'),
    path('list_department', ListDepartmentView.as_view(), name='list_department'),
    path('list_student_files/<programme_id>/<dept_id>', ListFilesView.as_view(), name='list_student_files'),
    path('delete_stud_files/<pk>', DeleteStudentFilesView.as_view(), name='delete_stud_files'),
    path('list_student/<programme_id>/<dept_id>', ListStudentView.as_view(), name='list_student'),

    # # Files(Supervisors)
    path('files_super/<str:dept_id>', SupervisorFilesView.as_view(), name='files_super'),
    path('list_super_files/<str:dept_id>', ListSupervisorFilesView.as_view(), name='list_super_files'),
    path('delete_super_files/<pk>', DeleteSupervisorFilesView.as_view(), name='delete_super_files'),
    path('list_supervisor/<dept_id>', ListSupervisorView.as_view(), name='list_supervisor'),


    # Manage Students
    path('manage_students/<str:dept_id>', ManageStudentsView.as_view(), name='manage_students'),
    path('delete_user/<str:user_id>', DeleteUserAccountView.as_view(), name='delete_user'),

    # Manage Administrators
    path('manage_administrators', ManageAdministratorsView.as_view(), name='manage_administrators'),

    # Manage Supervisors
    path('manage_supervisors/<str:dept_id>', ManageSupervisorsView.as_view(), name='manage_supervisors'),

    # Profile
    path('manage_profile/<str:user_id>', ManageProfileView.as_view(), name='manage_profile'),

    # Email
    path('reverify_email', ReVerifyEmailView.as_view(), name='reverify_email'),
    path('resend_email', ResendEmailVerificationView.as_view(), name='resend_email'),
    path('verify/<uidb64>/<token>', EmailActivationView.as_view(), name='verify'),
    path('reset_password', ResetPasswordView.as_view(), name='reset_password'),
    path('complete_reset_password/<uidb64>/<token>', ResetPasswordActivationView.as_view(), name='complete_reset_password'),

    # Settings
    path('settings', SettingsView.as_view(), name='settings'),

    # Settings
    path('notifications', NotificationsView.as_view(), name='notifications'),

    # Help
    path('help', HelpView.as_view(), name='help'),

    # Department
    path('department/<str:dept_id>', DepartmentView.as_view(), name='department'),
    path('what_file/<str:dept_id>', WhatFileView.as_view(), name='what_file'),
    path('batch_create/<str:dept_id>/<int:file_id>', BatchCreateView.as_view(), name='batch_create'),

    # Manage Coordinators
    path('manage_coordinators/<str:dept_id>', ManageCoordinatorsView.as_view(), name='manage_coordinators'),

    # Allocate Students
    path('allocate/<str:dept_id>', AllocateView.as_view(), name='allocate'),
    path('manage_allocate/<str:dept_id>', ManageAllocationsView.as_view(), name='manage_allocate'),

    path('assigned_students', AssignedStudentView.as_view(), name='assigned_students'),
    path('assigned_supervisor', AssignedSupervisorView.as_view(), name='assigned_supervisors'),
    path('display_group_members/<str:group_id>', DisplayGroupMembersView.as_view(), name='display_group_members'),

    # Student Dashboard
    # path may be 'dashboard/CST20HND1231'
    path('student_dashboard', StudentDashboardView.as_view(), name='student_dashboard')

]
