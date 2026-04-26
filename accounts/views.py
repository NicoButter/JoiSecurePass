from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserForm, AddressFormSet, PhoneFormSet
from .models import CustomUser
import base64
import io
import json
import numpy as np

try:
    from PIL import Image
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False

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
    return render(request, 'accounts/operativo_dashboard.html')

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
    from django.shortcuts import redirect
    return redirect('admin_dashboard')


def operativo_dashboard(request):
    from django.shortcuts import redirect
    return redirect('operativo_dashboard')

# --------------------------------------------------------------------------------------------

def personal_registration(request):
    return render(request, 'accounts/personal_registration.html')


# --------------------------------------------------------------------------------------------
# ENROLLMENT BIOMÉTRICO
# --------------------------------------------------------------------------------------------

@login_required
def enroll_face(request, pk):
    """
    GET  → muestra la interfaz de captura biométrica para el usuario pk.
    POST → recibe un frame base64, extrae el encoding y lo acumula en la sesión.
           Cuando el cliente envía finish=true, promedia todos los encodings
           acumulados y guarda el vector final en CustomUser.face_encoding.
    Solo accesible por administradores.
    """
    target_user = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'GET':
        request.session['enroll_encodings'] = []
        return render(request, 'accounts/enroll_face.html', {'target_user': target_user})

    elif request.method == 'POST':
        if not FACE_RECOGNITION_AVAILABLE:
            return JsonResponse({'error': 'face_recognition no está instalado'}, status=500)

        finish = request.POST.get('finish') == 'true'

        if finish:
            encodings = request.session.get('enroll_encodings', [])
            if len(encodings) < 3:
                return JsonResponse({'error': 'Se necesitan al menos 3 capturas válidas'}, status=400)

            avg_encoding = np.mean(np.array(encodings), axis=0).tolist()
            target_user.face_encoding = avg_encoding
            target_user.save(update_fields=['face_encoding'])
            request.session.pop('enroll_encodings', None)
            return JsonResponse({
                'status': 'ok',
                'message': f'Enrollment completado con {len(encodings)} capturas.',
                'samples': len(encodings),
            })

        # Procesar frame individual
        image_data = request.POST.get('image', '')
        if not image_data:
            return JsonResponse({'error': 'No se recibió imagen'}, status=400)

        try:
            if ',' in image_data:
                image_data = image_data.split(',', 1)[1]
            image = Image.open(io.BytesIO(base64.b64decode(image_data))).convert('RGB')
            image_np = np.array(image)

            encodings = face_recognition.face_encodings(image_np)
            if not encodings:
                return JsonResponse({'status': 'no_face'})

            accumulated = request.session.get('enroll_encodings', [])
            accumulated.append(encodings[0].tolist())
            request.session['enroll_encodings'] = accumulated
            request.session.modified = True

            return JsonResponse({'status': 'captured', 'count': len(accumulated)})

        except Exception as e:
            print(f"Error en enrollment: {e}")
            return JsonResponse({'error': 'Error al procesar la imagen'}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
