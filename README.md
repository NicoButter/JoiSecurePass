# JoiSecurePass: Sistema de Control de Acceso Basado en Reconocimiento Facial y NFC

## Descripción general
**JoiSecurePass** es una aplicación web desarrollada con **Django** y **PostgreSQL** diseñada para gestionar de manera eficiente el control de acceso del personal en una organización. El sistema combina tecnologías de reconocimiento facial y **NFC** para registrar los ingresos y salidas de los empleados, generando reportes detallados sobre su actividad laboral.

## Funcionalidades principales
- **Reconocimiento facial**: Permite identificar a los empleados a través de una cámara web y una base de datos de rostros.
- **Registro de ingresos y salidas**: Registra de manera precisa la hora de entrada y salida de cada empleado.
- **Control de acceso mediante NFC**: Permite el registro de ingresos y salidas utilizando tarjetas o dispositivos NFC.
- **Generación de reportes**: Genera reportes personalizados sobre la actividad de los empleados, incluyendo horas extras, faltas, horas de menos, etc.
- **Integración con PostgreSQL**: Utiliza PostgreSQL como base de datos para almacenar la información de los empleados, los registros de acceso y los reportes.

## Tecnologías utilizadas
- **Django**: Framework web para el desarrollo de la aplicación.
- **PostgreSQL**: Base de datos relacional para almacenar la información.
- **OpenCV**: Biblioteca de visión por computadora para el reconocimiento facial.
- **[Biblioteca para NFC]**: Especifica la biblioteca utilizada para la interacción con dispositivos NFC.
- **[Otras bibliotecas relevantes]**: Menciona otras bibliotecas utilizadas, como por ejemplo para la generación de reportes.

## Requisitos del sistema
- **Sistema operativo**: OpenSUSE
- **Python**: [Versión de Python utilizada]
- **Django**: [Versión de Django utilizada]
- **PostgreSQL**: [Versión de PostgreSQL utilizada]
- **[Otras dependencias]**: Enumera otras dependencias necesarias.

## Instalación y configuración
1. **Clonar el repositorio**:
   ```bash
   git clone https://[tu_repositorio] JoiSecurePass

   Crear y activar el entorno virtual:

`...
python -m venv venv
source venv/bin/activate
...`

`...
Instalar las dependencias:

pip install -r requirements.txt
Configurar la base de datos:

bash
Copiar código

# Editar el archivo settings.py con los datos de tu base de datos PostgreSQL


Ejecutar las migraciones:


python manage.py migrate
Iniciar el servidor de desarrollo:
...`


python manage.py runserver
Estructura del proyecto
[Estructura de directorios] (Describe brevemente la estructura de tu proyecto)

Contribuciones
¡Las contribuciones son bienvenidas! Si deseas contribuir a este proyecto, por favor, sigue estos pasos:

Forkea el repositorio.
Crea una nueva rama.
Realiza tus cambios.
Envía una solicitud de pull.
Licencia
Este proyecto está bajo la licencia MIT.