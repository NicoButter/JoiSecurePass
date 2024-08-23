import face_recognition
import numpy as np
from PIL import Image
import io
from django.core.files.base import ContentFile
from .attendance.models import CustomUser, Attendance

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
    unknown_face_encoding = face_recognition.face_encodings(image)
    
    if not unknown_face_encoding:
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

def record_attendance(user):
    from django.utils import timezone
    now = timezone.now()
    attendance, created = Attendance.objects.get_or_create(user=user, date=now.date())
    if created:
        attendance.check_in_time = now.time()
    else:
        attendance.check_out_time = now.time()
    attendance.save()
