import base64
import face_recognition
import numpy as np
from PIL import Image
import io
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .attendance.models import CustomUser, Attendance

def recognize_face(image_data):
    # Convertir la imagen base64 a imagen
    try:
        image_data = image_data.split(',')[1]  # Separa los metadatos del contenido base64
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        image = np.array(image)
    except Exception as e:
        print(f"Error al decodificar la imagen: {e}")
        return None

    # Obtener imágenes de usuarios registrados
    users = CustomUser.objects.all()
    known_face_encodings = []
    known_face_names = []

    for user in users:
        if user.profile_image:
            try:
                user_image = face_recognition.load_image_file(user.profile_image.path)
                face_encoding = face_recognition.face_encodings(user_image)[0]
                known_face_encodings.append(face_encoding)
                known_face_names.append(user.username)
            except Exception as e:
                print(f"Error al procesar la imagen del usuario {user.username}: {e}")

    # Buscar rostros en la imagen recibida
    unknown_face_encoding = face_recognition.face_encodings(image)
    
    if not unknown_face_encoding:
        print("No se encontró ninguna cara en la imagen proporcionada.")
        return None
    
    matches = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding[0])
    
    if True in matches:
        matched_idx = matches.index(True)
        user_name = known_face_names[matched_idx]
        user = CustomUser.objects.get(username=user_name)
        
        # Registrar la entrada o salida
        record_attendance(user)
        return user_name
    
    return None

@csrf_exempt
def record_attendance(request):
    if request.method == 'POST':
        # Procesar el formulario y la imagen enviada
        image_data = request.POST.get('image')
        if image_data:
            user_name = recognize_face(image_data)
        
            if user_name:
                return JsonResponse({'message': f"Asistencia registrada para {user_name}"})
            else:
                return JsonResponse({'message': "No se reconoció ningún rostro"}, status=400)
        else:
            return JsonResponse({'message': "No se recibió ninguna imagen."}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)
