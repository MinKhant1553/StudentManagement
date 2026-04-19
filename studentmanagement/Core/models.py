from django.db import models
from datetime import timezone
from django.contrib.auth.models import User
from django.utils import timezone
    
class Student(models.Model):
    Classes = [
        ('English', 'English'),
        ('French', 'French'),
        ('German', 'German'),
        ('Spanish', 'Spanish'),
        ('Italian', 'Italian'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phonenum = models.CharField(max_length=15, blank=True, null=True)   
    age = models.IntegerField()
    class_type = models.CharField(max_length=30, choices=Classes, default='English')
    enrolled_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(max_length=200, blank=True, null=True)

    def full_name(self):
        return f"{self.fname} {self.lname}"

    def __str__(self):
        return self.full_name()
    
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=100)
    hired_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def full_name(self):
        return f"{self.fname} {self.lname}"

    def __str__(self):
        return f"{self.fname} {self.lname} {self.subject}"
    
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,default= None, related_name='courses')
    students = models.ManyToManyField(Student, blank=True , related_name='courses')
    created_date = models.DateField(auto_now_add=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Attendance(models.Model):
    status_choices = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=status_choices)

    class Meta:
        unique_together = ('student', 'course', 'date') # to ensures that a student can only have one attendance record per course per day

    def __str__(self):
        return f"{self.student.full_name()} - {self.course.name} on {self.date}: {self.status}"
    