from django.shortcuts import render
from .models import Student
from .forms import StudentForm

# Create your views here.
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse

from .models import Student
from .forms import StudentForm, RegisterForm


# ─── Auth Views ────────────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('student_list')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Account created! Please log in.")
        return redirect('login')
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('student_list')
    error = None
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'student_list'))
        error = "Invalid username or password."
    return render(request, 'registration/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── Dashboard ─────────────────────────────────────────────────────────────────

@login_required
def dashboard_view(request):
    total = Student.objects.count()
    recent = Student.objects.order_by('-date_of_admission')[:5]
    courses = Student.objects.values_list('course', flat=True).distinct()
    return render(request, 'students/dashboard.html', {
        'total': total,
        'recent': recent,
        'courses': courses,
    })


# ─── Student CRUD ──────────────────────────────────────────────────────────────

@login_required
def student_list(request):
    query = request.GET.get('q', '')
    course_filter = request.GET.get('course', '')
    students = Student.objects.all()

    if query:
        students = students.filter(full_name__icontains=query)
    if course_filter:
        students = students.filter(course__icontains=course_filter)

    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'students/student_list.html', {
        'page_obj': page_obj,
        'query': query,
        'course_filter': course_filter,
    })


@login_required
def student_add(request):
    form = StudentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Student added successfully!")
        return redirect('student_list')
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add Student'})


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Student updated successfully!")
        return redirect('student_list')
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Edit Student', 'student': student})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if not request.user.is_superuser:
        messages.error(request, "Only superusers can delete students.")
        return redirect('student_list')
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})


# ─── CSV Export ────────────────────────────────────────────────────────────────

@login_required
def export_csv(request):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students.csv"'
        writer = csv.writer(response)
        writer.writerow(['Full Name', 'Email', 'Phone', 'Course', 'Date of Admission'])
        for s in Student.objects.all():
            writer.writerow([s.full_name, s.email, s.phone, s.course, s.date_of_admission])
        return response
    except Exception as e:
        from django.contrib import messages
        messages.error(request, f"Export failed: {str(e)}")
        return redirect('student_list')
