# Campus Café

Sistema de gestión de pedidos para la cafetería "Campus Café".

## Propósito

Gestionar la captura, cobro, preparación y entrega de pedidos de alimentos, evitando la pérdida de comandas y la doble fila de los estudiantes.

## Equipo

Equipo 15: Alison Astrid Uribe López y Emiliano Covarrubias Toledo.

Nota: la construcción y documentación de E1 y E2 fue realizada por Alison Astrid Uribe López.

## Tipo de aplicación y stack

Aplicación web.

- Python 3.14.8
- Django 6.1.2
- PostgreSQL 16.15
- psycopg 3.3.6
- Visual Studio Code 1.144.0
- Git 2.56.0 y GitHub

## Estado

- **E1:** entorno y base de datos preparados. La conexión aplicación-BD se demuestra con la ruta técnica `/estado-bd/`, que consulta el número de alumnos y productos registrados.
- **E2:** construcción incremental de los casos de uso CU-01 a CU-05, con inicio de sesión por puesto, base de datos integrada y commits progresivos.

## Instalación y ejecución

1. Clonar el repositorio y entrar a la carpeta del proyecto: `git clone https://github.com/alisonurlop/campus-cafe.git` y luego `cd campus-cafe`
2. Crear y activar el entorno virtual (Windows): `python -m venv venv` y luego `venv\Scripts\activate`
3. Instalar dependencias: `pip install -r requirements.txt`
4. En PostgreSQL (pgAdmin) crear un usuario `campus_user` con contraseña propia y una base de datos `campus_cafe` cuyo dueño sea ese usuario.
5. Copiar `.env.example` como `.env` y escribir ahí la contraseña real. El proyecto carga este archivo con la librería python-dotenv desde `config/settings.py`.
6. Crear las tablas: `python manage.py migrate`
7. Crear un administrador: `python manage.py createsuperuser`
8. Iniciar la aplicación: `python manage.py runserver`
9. Abrir `http://127.0.0.1:8000/estado-bd/` para ver la consulta técnica de conexión.
10. Entrar a `http://127.0.0.1:8000/admin/` para cargar datos ficticios: alumnos (con matrícula), productos y empleados.

Para volver a ejecutar el proyecto en otra sesión: abrir la terminal en la carpeta del proyecto, activar el entorno (`venv\Scripts\activate`) y correr `python manage.py runserver`.

## Uso del sistema

Los empleados se crean en `/admin/`: primero un usuario (Users) y después su registro en Empleados, con puesto Cajero o Cocinero.

| Rol | Ruta | Qué hace |
|---|---|---|
| Cajero | `/login/` | Catálogo, ticket, matrícula del alumno, "Cobrar y Transmitir" y "Cancelar orden". Muestra alertas de incidencias. |
| Cocinero | `/login/` | Lista de pedidos pendientes, "Listo para entregar", "Marcar como entregado" y "Registrar incidencia". |
| Estudiante | `/estado/` | Sin login. Consulta el estado de su pedido con su matrícula. |

Después de iniciar sesión, el sistema redirige según el puesto del empleado.

## Casos de uso implementados

| Caso de uso | Descripción | Requisitos |
|---|---|---|
| CU-01 | Registrar pedido | RF-01, RF-02, RF-03 |
| CU-02 | Consultar órdenes pendientes | RF-04, RF-05 |
| CU-03 | Actualizar estado del pedido | RF-06, RF-07 |
| CU-04 | Consultar estado del pedido | RF-08 |
| CU-05 | Registrar incidencia | RF-09 |

Validaciones y errores manejados: matrícula no registrada, ticket vacío, incidencia sin descripción y restricción de pantallas por puesto.

## Estructura del código

- `config/`: configuración del proyecto y ruta técnica `/estado-bd/`.
- `alumnos/`, `catalogo/`, `empleados/`: modelos y administración de alumnos, productos y empleados.
- `pedidos/`: modelos (Pedido, DetallePedido, Incidencia), vistas, rutas y plantillas de los casos de uso.

## Base de datos

Modelo de U2 implementado con migraciones de Django (alumnos, catalogo, empleados y pedidos). La BD se crea ejecutando `python manage.py migrate`. No se usa un script SQL aparte.

Ajustes respecto a U2, detectados durante E3: se agregó `matricula` en ALUMNO y `precio_aplicado` en DETALLE_PEDIDO; EMPLEADO se liga al usuario de autenticación de Django.

## Datos

Solo se usan datos ficticios. No se incluyen datos personales reales.