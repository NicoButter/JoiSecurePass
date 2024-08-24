from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserForm, AddressFormSet, PhoneFormSet
from .models import CustomUser

def landing_page(request):
    return render(request, 'accounts/landing_page.html')

# --------------------------------------------------------------------------------------------

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.nivel_acceso.nombre == 'Administrador':
                return redirect('admin_dashboard')
            elif user.nivel_acceso.nombre == 'Operativo':
                return redirect('operativo_dashboard')
            else:
                return redirect('record_attendance')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# --------------------------------------------------------------------------------------------

def operativo_dashboard(request):
    return render(request, 'attendance/operativo_dashboard.html')

# --------------------------------------------------------------------------------------------

def logout_view(request):
    auth_logout(request)
    return redirect('login')

# --------------------------------------------------------------------------------------------

def register(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST)
        address_formset = AddressFormSet(request.POST, instance=None)
        phone_formset = PhoneFormSet(request.POST, instance=None)
        
        if user_form.is_valid() and address_formset.is_valid() and phone_formset.is_valid():
            user = user_form.save()
            addresses = address_formset.save(commit=False)
            phones = phone_formset.save(commit=False)
            
            for address in addresses:
                address.user = user
                address.save()
                
            for phone in phones:
                phone.user = user
                phone.save()
            
            return redirect('login')
    else:
        user_form = CustomUserForm()
        address_formset = AddressFormSet(instance=None)
        phone_formset = PhoneFormSet(instance=None)
    
    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'address_formset': address_formset,
        'phone_formset': phone_formset,
    })

# --------------------------------------------------------------------------------------------

def edit_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=user)
        address_formset = AddressFormSet(request.POST, instance=user)
        phone_formset = PhoneFormSet(request.POST, instance=user)
        
        if user_form.is_valid() and address_formset.is_valid() and phone_formset.is_valid():
            user = user_form.save()
            addresses = address_formset.save(commit=False)
            phones = phone_formset.save(commit=False)
            
            for address in addresses:
                address.user = user
                address.save()
                
            for phone in phones:
                phone.user = user
                phone.save()
            
            return redirect('user_detail', pk=user.pk)
    else:
        user_form = CustomUserForm(instance=user)
        address_formset = AddressFormSet(instance=user)
        phone_formset = PhoneFormSet(instance=user)
    
    return render(request, 'accounts/edit_user.html', {
        'user_form': user_form,
        'address_formset': address_formset,
        'phone_formset': phone_formset,
    })

# --------------------------------------------------------------------------------------------

def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'accounts/user_detail.html', {'user': user})

# --------------------------------------------------------------------------------------------

def admin_dashboard(request):
    # Vista para el dashboard de administración
    return render(request, 'accounts/admin_dashboard.html')

# --------------------------------------------------------------------------------------------

def personal_registration(request):
    # Vista para el registro de personal
    return render(request, 'accounts/personal_registration.html')
