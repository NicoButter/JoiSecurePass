from django.shortcuts import render, redirect
from .models import Attendance
from .forms import AttendanceForm, AttendanceSearchForm

def record_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST, request.FILES)  # Incluye request.FILES para archivos
        if form.is_valid():
            form.save()
            return redirect('attendance_record_success')  # Asegúrate de definir esta URL
    else:
        form = AttendanceForm()
    return render(request, 'attendance/record_attendance.html', {'form': form})

def search_attendance(request):
    if request.method == 'POST':
        form = AttendanceSearchForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            user = form.cleaned_data.get('user')
            filters = {}
            if date:
                filters['date'] = date
            if user:
                filters['user'] = user

            attendances = Attendance.objects.filter(**filters)
            return render(request, 'attendance/search_results.html', {'attendances': attendances, 'form': form})
    else:
        form = AttendanceSearchForm()
    return render(request, 'attendance/search_attendance.html', {'form': form})
