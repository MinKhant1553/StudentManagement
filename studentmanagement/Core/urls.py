from django.urls import path
from . import views

urlpatterns = [
    # Define your URL patterns here
    path('', views.Home, name='home'),
    # Authentication URLs
    path('login/', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    path('logout/', views.Logout, name='logout'),
    # Student URLs
    path('studentlist/', views.StudentList, name='studentlist'),
    path('students/<int:student_id>/', views.StudentDetails, name='student_details'),
    path('students/add/', views.AddStudent, name='add_student'),
    path('students/confirm_delete/<int:student_id>/', views.StudentConfirmDelete, name='student_confirm_delete'),
    path('students/edit/<int:student_id>/', views.StudentEdit, name='student_edit'),
    #course URL
    path('courselist/', views.CourseList, name='course_list'),
    path('courses/<int:course_id>/', views.CourseDetails, name='course_details'),
    path('courses/enroll/<int:course_id>/', views.EnrollCourse, name='enroll_course'),
    # attendance URL
    path ('courses/attendance/mark/<int:course_id>/<int:student_id>/', views.MarkAttendance, name='mark_attendance'),
]