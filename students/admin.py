from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'course', 'date_of_admission']
    search_fields = ['full_name', 'email', 'course']
    list_filter = ['course', 'date_of_admission']
    ordering = ['-date_of_admission']