from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import io
import json
import numpy as np
from PIL import Image
from accounts.models import CustomUser
from .models import Attendance
from django.utils import timezone

try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False


@csrf_exempt
def record_attendance(request):
    if request.method == 'GET':
        return render(request, 'attendance/record_attendance.html')

    elif request.method == 'POST':
        image_data = request.POST.get('image')

        if not image_data:
            return JsonResponse({'error': "No se recibió ninguna imagen."}, status=400)

        try:
            if ',' in image_data:
                image_data = image_data.split(',', 1)[1]
            else:
                raise ValueError("Formato de datos de imagen incorrecto")

            result = recognize_face(image_data)

            if result:
                return JsonResponse(result)
            else:
                return JsonResponse({'error': "No se reconoció ningún rostro"}, status=400)
        except Exception as e:
            print(f"Error al procesar la imagen: {e}")
            return JsonResponse({'error': 'Error en el procesamiento de la imagen'}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


def recognize_face(image_data):
    """
    Compara el frame capturado contra los encodings almacenados en la BD.
    No carga ni procesa ninguna imagen de archivo — sólo vectores numéricos.
    """
    try:
        image = Image.open(io.BytesIO(base64.b64decode(image_data))).convert('RGB')
        image_np = np.array(image)

        # Cargar encodings desde la BD (sólo usuarios con encoding registrado)
        users = CustomUser.objects.exclude(face_encoding__isnull=True)
        known_encodings = []
        known_users = []

        for user in users:
            encoding = np.array(user.face_encoding, dtype=np.float64)
            known_encodings.append(encoding)
            known_users.append(user)

        if not known_encodings:
            return None

        # Detectar rostro en el frame actual
        unknown_encodings = face_recognition.face_encodings(image_np)
        if not unknown_encodings:
            return None

        # Comparar con tolerancia estándar (0.6); distancias para elegir el mejor match
        distances = face_recognition.face_distance(known_encodings, unknown_encodings[0])
        best_idx = int(np.argmin(distances))

        if distances[best_idx] <= 0.55:  # umbral más estricto para reducir falsos positivos
            user = known_users[best_idx]
            action, registered_time = record_attendance_entry(user)
            full_name = user.get_full_name() or user.username
            return {
                'name': full_name,
                'action': action,
                'time': registered_time,
            }

        return None

    except (ValueError, base64.binascii.Error, IOError, IndexError) as e:
        print(f"Error en el reconocimiento facial: {e}")
        return None


def record_attendance_entry(user):
    now = timezone.now()
    attendance, created = Attendance.objects.get_or_create(user=user, date=now.date())
    if created:
        attendance.check_in_time = now.time()
        action = 'ENTRADA'
    else:
        attendance.check_out_time = now.time()
        action = 'SALIDA'
    attendance.save()
    local_time = timezone.localtime(now)
    return action, local_time.strftime('%H:%M')

    if request.method == 'GET':
        return render(request, 'attendance/record_attendance.html')

    elif request.method == 'POST':
        image_data = request.POST.get('image')

        if not image_data:
            return JsonResponse({'error': "No se recibió ninguna imagen."}, status=400)

        try:
            if ',' in image_data:
                image_data = image_data.split(',', 1)[1]
            else:
                raise ValueError("Formato de datos de imagen incorrecto")

            result = recognize_face(image_data)

            if result:
                return JsonResponse(result)
            else:
                return JsonResponse({'error': "No se reconoció ningún rostro"}, status=400)
        except Exception as e:
            print(f"Error al procesar la imagen: {e}")
            return JsonResponse({'error': 'Error en el procesamiento de la imagen'}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def recognize_face(image_data):
    try:
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        image = np.array(image)

        users = CustomUser.objects.all()
        known_face_encodings = []
        known_face_users = []

        for user in users:
            if user.profile_image:
                user_image = face_recognition.load_image_file(user.profile_image.path)
                face_encodings = face_recognition.face_encodings(user_image)
                if face_encodings:
                    known_face_encodings.append(face_encodings[0])
                    known_face_users.append(user)

        unknown_face_encodings = face_recognition.face_encodings(image)

        if not unknown_face_encodings:
            return None

        matches = face_recognition.compare_faces(known_face_encodings, unknown_face_encodings[0])

        if True in matches:
            matched_idx = matches.index(True)
            user = known_face_users[matched_idx]

            action, registered_time = record_attendance_entry(user)

            full_name = user.get_full_name() or user.username
            return {
                'name': full_name,
                'action': action,
                'time': registered_time,
            }

        return None

    except (ValueError, base64.binascii.Error, IOError, IndexError) as e:
        print(f"Error en el reconocimiento facial: {e}")
        return None

def record_attendance_entry(user):
    now = timezone.now()
    attendance, created = Attendance.objects.get_or_create(user=user, date=now.date())
    if created:
        attendance.check_in_time = now.time()
        action = 'ENTRADA'
    else:
        attendance.check_out_time = now.time()
        action = 'SALIDA'
    attendance.save()
    local_time = timezone.localtime(now)
    return action, local_time.strftime('%H:%M')
