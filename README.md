# Joi Secure Pass 

## Sistema de Control de Acceso Basado en Reconocimiento Facial y NFC

![](images/joisecurepass.png)

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

## Requisitos del sistema
- **Sistema operativo**: OpenSUSE (porque a mi me gusta mucho)
- **Python**: [3.11]
- **Django**: [4]
- **PostgreSQL**: []


## Instalación y configuración
1. **Clonar el repositorio**:
   ```sh
      git clone https://[tu_repositorio] JoiSecurePass
   ```

2. Crear y activar el entorno virtual:
   ```sh
      python -m venv venv
      source venv/bin/activate
   ```
   
Instalar las dependencias:
   ```sh
      pip install -r requirements.txt
   ```

3. Configurar la base de datos:

   Editar el archivo settings.py con los datos de tu base de datos PostgreSQL


4. Ejecutar las migraciones:
   ```sh
      python manage.py migrate
   ```

Iniciar el servidor de desarrollo:
   ```sh
      python manage.py runserver
   ```

   ```sh
      git clone https://NicoButter/JoiSecurePassoiSecurePass
   ```

2. Crear y activar el entorno virtual:
   ```sh
     python -m venv venv
      source venv/bin/activate
   ```

3. Instalar las dependencias:
   ```sh
      pip install -r requirements.txt
   ```

4. Configurar la base de datos:

# Editar el archivo settings.py con los datos de tu base de datos.

Ejecutar las migraciones:
   ```sh
      python manage.py migrate
   ```

# Iniciar el servidor de desarrollo:
   ```sh
      python manage.py runserver
   ```

Contribuciones
¡Las contribuciones son bienvenidas! Si deseas contribuir a este proyecto, por favor, sigue estos pasos:

Forkea el repositorio.
Crea una nueva rama.
Realiza tus cambios.
Envía una solicitud de pull.

# Licencia
## Este proyecto está bajo la licencia MIT.

### Si tienes alguna pregunta o sugerencia sobre este proyecto, no dudes en abrir un issue en el repositorio o contactarme a través de nicobutter@gmail.com.

Este proyecto está bajo la licencia MIT.
