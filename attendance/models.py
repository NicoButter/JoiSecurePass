from django.db import models
from django.conf import settings  # Importa settings para usar AUTH_USER_MODEL

class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    photo = models.ImageField(upload_to='attendance_photos/', null=True, blank=True)  # Campo para la imagen

    def __str__(self):
        return f"{self.user.username} - {self.date}"
