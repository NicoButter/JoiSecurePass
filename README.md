# Joi Secure Pass

## Sistema de Control de Acceso Biomórtico y Gestión de Personal

![](images/joisecurepass.png)

## Descripción General
**JoiSecurePass** es una aplicación web moderna desarrollada en **Django 5.1** diseñada para gestionar de manera automatizada el control de acceso del personal. El sistema combina un diseño de vanguardia (*Glassmorphism / Cyberpunk*) con un motor de reconocimiento facial que prioriza la privacidad: en lugar de almacenar fotos, utiliza vectores matemáticos (`face_encodings` de 128 flotantes).

## Funcionalidades Principales
- **Arquitectura Biométrica Segura:** No se almacenan imágenes en el servidor. El enrolamiento captura 10 frames de video, los promedia y guarda únicamente un array matemático en la base de datos (JSONField).
- **Proceso de Enrolamiento en 2 Pasos:** 
  1. El administrador ingresa los datos personales del empleado (DNI, legajo, nivel de acceso).
  2. El sistema redirige a una terminal de captura web para generar el vector biométrico en tiempo real.
- **Terminal de Fichaje (Kiosco):** Interfaz inmersiva, sin botones de navegación, que se autoejecuta. Cada 2.5 segundos escanea el entorno, y al detectar un rostro calcula la distancia (threshold 0.55). Muestra validación con hora exacta, nombre del empleado y etiqueta de ENTRADA/SALIDA. Salida discreta (5 clics en el logo).
- **Interfaz UI/UX Moderna:** Diseño completamente responsivo basado en fondos tipo grilla (bg-grid), orbes de luz animados (Orbitron, Exo 2), tarjetas de *"Glassmorphism"*, inputs estilizados y compatibilidad con modo oscuro (`#1a1a2e`).
- **Autenticación Basada en Roles:** Diferenciación entre `Administrador` y nivel `Operativo`.

## Tecnologías Utilizadas
- **Backend:** Django 5.1, SQLite (actual) / PostgreSQL (soportado).
- **Computer Vision & Biometría:** `face_recognition` (basado en dlib), `OpenCV` / `Pillow`, `numpy`.
- **Frontend:** HTML5, Vanilla JS, CSS3 Nativo (Glassmorphism, Flexbox, CSS Variables).

## Requisitos del Sistema
- **Sistema Operativo:** Basado en Linux (ej. openSUSE). Compatible con Windows/macOS teniendo las dependencias de C++ para `dlib`.
- **Python:** 3.11+ (Recomendado 3.14)

## Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/NicoButter/JoiSecurePass.git
   cd JoiSecurePass
   ```

2. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # o `venv\Scripts\activate` en Windows
   ```
   
3. **Instalar las dependencias:**
   *(Requiere CMake y compilador C++ en el sistema para compilar dlib)*
   ```bash
   pip install -r requirements.txt
   ```

4. **Variables de Entorno (.env):**
   Crea un archivo `.env` en la raíz del proyecto para definir:
   ```ini
   SECRET_KEY=tu_clave_secreta
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   ```

5. **Ejecutar las migraciones:**
   Generará la base de datos `db.sqlite3` y aplicará los campos de `face_encoding`.
   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Iniciar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```
   *Accede a `http://127.0.0.1:8000` para ver la Landing Page.*

## Contribuciones
¡Las contribuciones son bienvenidas! Si deseas contribuir a este proyecto:
1. Haz un Fork del repositorio.
2. Crea una nueva rama para tu feature.
3. Realiza tus cambios y haz commits descriptivos.
4. Envía un Pull Request.

## Licencia
Este proyecto está bajo la licencia MIT.

### Contacto
Si tienes alguna pregunta, duda o sugerencia sobre este proyecto, no dudes en abrir un issue en el repositorio o contactarte con **Nicolas Buttefield** ([@nicobutter](https://github.com/nicobutter)) a través de **nicobutter@gmail.com**.

