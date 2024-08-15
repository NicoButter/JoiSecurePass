from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# ----------------------------------------------------------------------------------------------------------

class CustomUser(AbstractUser):
    dni = models.CharField(max_length=20, unique=True, blank=True, null=True)
    numero_legajo = models.CharField(max_length=50, unique=True, blank=True, null=True)
    nivel_acceso = models.ForeignKey('NivelAcceso', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username
  
# ----------------------------------------------------------------------------------------------------------

class NivelAcceso(models.Model):
    NIVEL_ADMINISTRADOR = 1
    NIVEL_OPERATIVO = 2
    NIVEL_POLIVALENTE = 3

    NIVELES = (
        (NIVEL_ADMINISTRADOR, 'Administrador'),
        (NIVEL_OPERATIVO, 'Operativo'),
        (NIVEL_POLIVALENTE, 'Polivalente'),
    )

    nivel = models.IntegerField(choices=NIVELES, unique=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_nivel_display()} - {self.nombre}"

# ----------------------------------------------------------------------------------------------------------    

class Registro(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fecha_hora_entrada = models.DateTimeField(default=timezone.now)
    fecha_hora_salida = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Registro de {self.user.username} - Entrada: {self.fecha_hora_entrada} / Salida: {self.fecha_hora_salida}"

# ----------------------------------------------------------------------------------------------------------

class Address(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='addresses')
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.country} - {self.postal_code}"

# ----------------------------------------------------------------------------------------------------------

class Phone(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='phones')
    phone_number = models.CharField(max_length=20)
    phone_type = models.CharField(max_length=20, choices=[('mobile', 'Mobile'), ('home', 'Home'), ('work', 'Work')])

    def __str__(self):
        return f"{self.phone_number} ({self.get_phone_type_display()})"

