from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import io
import numpy as np
from PIL import Image
import face_recognition
from accounts.models import CustomUser
from .models import Attendance
from django.utils import timezone

@csrf_exempt
def record_attendance(request):
    if request.method == 'GET':
        # Renderiza la página HTML para capturar la imagen
        return render(request, 'attendance/record_attendance.html')

    elif request.method == 'POST':
        image_data = request.POST.get('image')

        if not image_data:
            return JsonResponse({'message': "No se recibió ninguna imagen."}, status=400)

        try:
            if ',' in image_data:
                image_data = image_data.split(',', 1)[1]
            else:
                raise ValueError("Formato de datos de imagen incorrecto")

            user_name = recognize_face(image_data)

            if user_name:
                return JsonResponse({'message': f"Asistencia registrada para {user_name}"})
            else:
                return JsonResponse({'message': "No se reconoció ningún rostro"}, status=400)
        except Exception as e:
            print(f"Error al procesar la imagen: {e}")
            return JsonResponse({'message': 'Error en el procesamiento de la imagen'}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def recognize_face(image_data):
    try:
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        image = np.array(image)

        users = CustomUser.objects.all()
        known_face_encodings = []
        known_face_names = []

        for user in users:
            if user.profile_image:
                user_image = face_recognition.load_image_file(user.profile_image.path)
                face_encodings = face_recognition.face_encodings(user_image)
                if face_encodings:
                    known_face_encodings.append(face_encodings[0])
                    known_face_names.append(user.username)

        unknown_face_encodings = face_recognition.face_encodings(image)

        if not unknown_face_encodings:
            return None

        matches = face_recognition.compare_faces(known_face_encodings, unknown_face_encodings[0])

        if True in matches:
            matched_idx = matches.index(True)
            user_name = known_face_names[matched_idx]
            user = CustomUser.objects.get(username=user_name)

            record_attendance_entry(user)
            return user_name

        return None

    except (ValueError, base64.binascii.Error, IOError, IndexError) as e:
        print(f"Error en el reconocimiento facial: {e}")
        return None

def record_attendance_entry(user):
    now = timezone.now()
    attendance, created = Attendance.objects.get_or_create(user=user, date=now.date())
    if created:
        attendance.check_in_time = now.time()
    else:
        attendance.check_out_time = now.time()
    attendance.save()
