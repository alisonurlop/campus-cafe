# Campus Café

Sistema de gestión de pedidos para la cafetería "Campus Café".

## Propósito
Gestionar la captura, cobro, preparación y entrega de pedidos de alimentos, evitando la pérdida de comandas y la doble fila de los estudiantes.

## Equipo
Equipo 15: Alison Astrid Uribe López y Emiliano Covarrubias Toledo.

## Tipo de aplicación y stack
Aplicación web.
- Python 3.14.8
- Django 6.1.2
- PostgreSQL 16.15
- psycopg 3.3.6
- Visual Studio Code 1.144.0
- Git 2.56.0 y GitHub

## Estado E1
Entorno y base de datos preparados. La conexión aplicación-BD se demuestra con la ruta técnica `/estado-bd/`, que consulta el número de alumnos y productos registrados. Los casos de uso se construirán en E2.

## Instalación y ejecución
1. Clonar el repositorio y entrar a la carpeta del proyecto.
2. Crear y activar el entorno virtual (Windows):
   `python -m venv venv` y luego `venv\Scripts\activate`
3. Instalar dependencias: `pip install -r requirements.txt`
4. En PostgreSQL (pgAdmin) crear un usuario `campus_user` con contraseña propia y una base de datos `campus_cafe` cuyo dueño sea ese usuario.
5. Copiar `.env.example` como `.env` y escribir ahí la contraseña real. El proyecto carga este archivo con la librería python-dotenv desde `config/settings.py`.
6. Crear las tablas: `python manage.py migrate`
7. Crear un administrador: `python manage.py createsuperuser`
8. Iniciar la aplicación: `python manage.py runserver`
9. Abrir `http://127.0.0.1:8000/estado-bd/` para ver la consulta técnica.
10. Opcional: entrar a `http://127.0.0.1:8000/admin/` para cargar alumnos y productos ficticios.

## Base de datos
Modelo de U2 implementado con migraciones de Django (alumnos, catalogo, empleados y pedidos). La BD se crea ejecutando `python manage.py migrate`. No se usa un script SQL aparte.

Ajustes respecto a U2, detectados durante E3: se agregó `matricula` en ALUMNO y `precio_aplicado` en DETALLE_PEDIDO; EMPLEADO se liga al usuario de autenticación de Django.

## Datos
Solo se usan datos ficticios. No se incluyen datos personales reales.