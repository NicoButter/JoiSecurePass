from django.shortcuts import render, redirect
from .models import Attendance
from .forms import AttendanceForm, AttendanceSearchForm

def record_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_record_success')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/record_attendance.html', {'form': form})

def search_attendance(request):
    if request.method == 'POST':
        form = AttendanceSearchForm(request.POST)
        if form.is_valid():
            # Filtrar y mostrar los resultados
            pass
    else:
        form = AttendanceSearchForm()
    return render(request, 'attendance/search_attendance.html', {'form': form})
