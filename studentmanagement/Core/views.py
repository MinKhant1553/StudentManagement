from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db import transaction
from .models import Student, Course, Attendance
from .forms import StudentForm, RegisterForm

# Create your views here.
def user_is_staff(user):
    return user.is_staff

def Home(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_staff:
            context['students_count'] = Student.objects.count()
            context['active_courses_count'] = Course.objects.count()
        else:
            if hasattr(request.user, 'student'):
                student = request.user.student
                count = student.courses.count()
                print(f"User: {request.user}, Student: {student.full_name}, Courses: {count}")
                context['my_courses_count'] = request.user.student.courses.count()
    return render(request, 'index.html', context)

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('home')

def Register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save()
                    student = student_form.save(commit=False)
                    student.user = user  # Link the student to the newly created user
                    student.save()
                    messages.success(request, 'Registration successful! You can now log in.')
                    return redirect('login')

            except Exception as e:
                # Handle the exception (e.g., log it, display an error message)
                pass
                # This will show you EXACTLY why it failed in your terminal
                print("USER FORM ERRORS:", user_form.errors)
                print("STUDENT FORM ERRORS:", student_form.errors)
    else:
        user_form = RegisterForm()
        student_form = StudentForm()
    return render(request, 'register.html', {'user_form': user_form, 'student_form': student_form})

@user_passes_test(user_is_staff)
def StudentList(request):
    students = Student.objects.all()
    return render(request, 'studentlist.html', {'students': students})

def StudentDetails(request, student_id):
    student = get_object_or_404(Student, id=student_id)    
    return render(request, 'student_details.html', {'student': student})

@user_passes_test(user_is_staff)
def AddStudent(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

@user_passes_test(user_is_staff)
def StudentEdit(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_details', student_id=student.id)
    else:
        form = StudentForm(instance=student)
    return render(request, 'editstudent.html', {'form': form, 'student': student})

@user_passes_test(user_is_staff)
def StudentConfirmDelete(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('studentlist')
    return render(request, 'confirm_delete.html', {'student': student})

def CourseList(request):
    courses = Course.objects.all()
    return render(request, 'courselist.html', {'courses': courses})

def CourseDetails(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    all_students = course.students.all()  # Get all students enrolled in this course
    return render(request, 'coursedetails.html', {'course': course, 'all_students': all_students})

@user_passes_test(user_is_staff)
def EnrollCourse(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, id=student_id)

        course.students.add(student)
        messages.success(request, f'{student.user.username} has been enrolled in {course.name}!')
        
    return redirect('course_details', course_id=course.id)

@user_passes_test(user_is_staff)
def MarkAttendance(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = course.students.all()  # Get all students enrolled in this course

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            Attendance.objects.update_or_create(
                student=student,
                course=course,
                defaults={'status': status}
            )
        messages.success(request, 'Attendance has been marked successfully!')
        return redirect('course_details', course_id=course.id)
    return render(request, 'mark_attendance.html', {'course': course, 'students': students})
