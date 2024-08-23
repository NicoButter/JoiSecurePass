from django.http import JsonResponse
from django.shortcuts import render
from .models import Attendance
from .forms import AttendanceForm, AttendanceSearchForm

def record_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            
            return JsonResponse({'message': '¡Asistencia registrada correctamente!'})
        else:
            return JsonResponse({'message': 'Error al registrar la asistencia. Verifica los datos ingresados.'}, status=400)
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
