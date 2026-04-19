from django.contrib import admin

from .models import Student, Teacher, Course, Attendance

# Register your models here.
admin.site.site_header = "Student Management Admin"
admin.site.site_title = "Welcome to Lingo Student Management Admin Portal"
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Attendance)