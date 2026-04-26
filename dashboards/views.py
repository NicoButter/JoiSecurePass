from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta, datetime, date
from django.db.models import Sum, Count, F, ExpressionWrapper, DurationField
from attendance.models import Attendance
from accounts.models import CustomUser, NivelAcceso

JORNADA_HORAS = 8  # horas de jornada normal diaria


def _calcular_horas(check_in, check_out):
    """Devuelve horas trabajadas como float. Retorna 0 si algún valor es None."""
    if check_in is None or check_out is None:
        return 0.0
    entrada = datetime.combine(date.today(), check_in)
    salida = datetime.combine(date.today(), check_out)
    diff = salida - entrada
    return max(diff.total_seconds() / 3600, 0)


@login_required
def operativo_dashboard(request):
    hoy = timezone.localdate()

    # Filtros de fecha
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')
    empleado_id = request.GET.get('empleado')

    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else hoy - timedelta(days=6)
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else hoy
    except ValueError:
        fecha_inicio = hoy - timedelta(days=6)
        fecha_fin = hoy

    registros_qs = Attendance.objects.filter(
        date__range=(fecha_inicio, fecha_fin)
    ).select_related('user').order_by('-date', 'user__username')

    if empleado_id:
        registros_qs = registros_qs.filter(user__id=empleado_id)

    # Enriquecer registros con horas trabajadas y horas extra
    registros = []
    total_horas = 0.0
    total_extra = 0.0
    ausencias = 0

    for r in registros_qs:
        horas = _calcular_horas(r.check_in_time, r.check_out_time)
        extra = max(horas - JORNADA_HORAS, 0)
        total_horas += horas
        total_extra += extra
        if r.check_in_time is None:
            ausencias += 1
        registros.append({
            'obj': r,
            'horas_trabajadas': round(horas, 2),
            'horas_extra': round(extra, 2),
        })

    # Registros del día de hoy
    registros_hoy = Attendance.objects.filter(date=hoy).select_related('user').order_by('user__username')
    hoy_data = []
    for r in registros_hoy:
        horas = _calcular_horas(r.check_in_time, r.check_out_time)
        hoy_data.append({
            'obj': r,
            'horas_trabajadas': round(horas, 2),
            'estado': 'Presente' if r.check_in_time else 'Ausente',
        })

    empleados = CustomUser.objects.filter(nivel_acceso__isnull=False).order_by('username')

    context = {
        'registros': registros,
        'registros_hoy': hoy_data,
        'empleados': empleados,
        'empleado_seleccionado': empleado_id,
        'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d'),
        'fecha_fin': fecha_fin.strftime('%Y-%m-%d'),
        'total_horas': round(total_horas, 2),
        'total_extra': round(total_extra, 2),
        'ausencias': ausencias,
        'jornada_horas': JORNADA_HORAS,
    }
    return render(request, 'dashboards/operativo_dashboard.html', context)


@login_required
def admin_dashboard(request):
    total_usuarios = CustomUser.objects.count()
    usuarios_por_nivel = NivelAcceso.objects.annotate(total=Count('customuser')).values('nombre', 'total')

    hoy = timezone.localdate()
    presentes_hoy = Attendance.objects.filter(date=hoy, check_in_time__isnull=False).count()
    ausentes_hoy = total_usuarios - presentes_hoy

    ultimos_registros = Attendance.objects.select_related('user').order_by('-date', '-check_in_time')[:10]

    ultimos_usuarios = CustomUser.objects.order_by('-date_joined')[:5]

    context = {
        'total_usuarios': total_usuarios,
        'usuarios_por_nivel': usuarios_por_nivel,
        'presentes_hoy': presentes_hoy,
        'ausentes_hoy': ausentes_hoy,
        'ultimos_registros': ultimos_registros,
        'ultimos_usuarios': ultimos_usuarios,
    }
    return render(request, 'dashboards/admin_dashboard.html', context)

