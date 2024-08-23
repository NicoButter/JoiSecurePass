import base64
import io
import numpy as np
from PIL import Image
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import CustomUser, Attendance
import face_recognition

@csrf_exempt
def record_attendance(request):
    if request.method == 'POST':
        # Procesar el formulario y la imagen enviada
        image_data = request.POST.get('image')
        user_name = recognize_face(image_data)
        
        if user_name:
            return JsonResponse({'message': f"Asistencia registrada para {user_name}"})
        else:
            return JsonResponse({'message': "No se reconoció ningún rostro"}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def recognize_face(image_data):
    # Convertir la imagen base64 a imagen
    image_data = image_data.split(',')[1]
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
    image = np.array(image)
    
    # Obtener imágenes de usuarios registrados
    users = CustomUser.objects.all()
    known_face_encodings = []
    known_face_names = []
    
    for user in users:
        if user.profile_image:
            user_image = face_recognition.load_image_file(user.profile_image.path)
            known_face_encodings.append(face_recognition.face_encodings(user_image)[0])
            known_face_names.append(user.username)
    
    # Buscar rostros en la imagen recibida
    unknown_face_encodings = face_recognition.face_encodings(image)
    
    if not unknown_face_encodings:
        return None
    
    matches = face_recognition.compare_faces(known_face_encodings, unknown_face_encodings[0])
    
    if True in matches:
        matched_idx = matches.index(True)
        user_name = known_face_names[matched_idx]
        user = CustomUser.objects.get(username=user_name)
        
        # Registrar la entrada o salida
        record_attendance_entry(user)
        return user_name
    
    return None

def record_attendance_entry(user):
    now = timezone.now()
    attendance, created = Attendance.objects.get_or_create(user=user, date=now.date())
    if created:
        attendance.check_in_time = now.time()
    else:
        attendance.check_out_time = now.time()
    attendance.save()
