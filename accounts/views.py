from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm
from .models import CustomUser

def landing_page(request):
    return render(request, 'accounts/landing_page.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.nivel_acceso.nombre in ['Administrador', 'Operativo']:
                return redirect('admin_dashboard')  # Redirige al dashboard de administración
            else:
                return redirect('personal_registration')  # Redirige al registro de personal
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def edit_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=user.pk)
    else:
        form = UserCreationForm(instance=user)
    return render(request, 'accounts/edit_user.html', {'form': form})

def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'accounts/user_detail.html', {'user': user})

def admin_dashboard(request):
    # Vista para el dashboard de administración
    return render(request, 'accounts/admin_dashboard.html')

def personal_registration(request):
    # Vista para el registro de personal
    return render(request, 'accounts/personal_registration.html')
