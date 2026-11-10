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
- python-dotenv (lectura del archivo `.env`)
- Visual Studio Code 1.144.0
- Git 2.56.0 y GitHub

## Estado

- **E1:** entorno y base de datos preparados. La conexión aplicación-BD se demuestra con la ruta técnica `/estado-bd/`.
- **E2:** casos de uso CU-01 a CU-05 funcionando, con inicio de sesión por puesto, base de datos integrada, control de productos agotados y commits progresivos.

## Instalación y ejecución

1. Clonar el repositorio y entrar a la carpeta del proyecto: `git clone https://github.com/alisonurlop/campus-cafe.git` y luego `cd campus-cafe`
2. Crear y activar el entorno virtual (Windows): `python -m venv venv` y luego `venv\Scripts\activate`
3. Instalar dependencias: `pip install -r requirements.txt`
4. En PostgreSQL (pgAdmin) crear un usuario `campus_user` con contraseña propia y una base de datos `campus_cafe` cuyo dueño sea ese usuario.
5. Copiar `.env.example` como `.env` y escribir ahí la contraseña real (ver "Configuración de la base de datos").
6. Crear las tablas: `python manage.py migrate`
7. Crear un administrador: `python manage.py createsuperuser`
8. Iniciar la aplicación: `python manage.py runserver`
9. Abrir `http://127.0.0.1:8000/estado-bd/` para ver la consulta técnica de conexión.
10. Entrar a `http://127.0.0.1:8000/admin/` para cargar datos ficticios: alumnos (con matrícula), productos y empleados.

Para volver a ejecutar el proyecto en otra sesión: abrir la terminal en la carpeta del proyecto, activar el entorno (`venv\Scripts\activate`) y correr `python manage.py runserver`.

## Configuración de la base de datos

El sistema usa PostgreSQL mediante el driver psycopg. Los datos de conexión (nombre de la base, usuario, contraseña, host y puerto) se leen del archivo `.env`, que **no se sube al repositorio** (está en `.gitignore`). El archivo `.env.example` muestra qué variables definir sin incluir contraseñas. La lectura se hace con python-dotenv en `config/settings.py`, dentro de `DATABASES`.

## Uso del sistema

Los empleados se crean en `/admin/`: primero un usuario (Users) y después su registro en Empleados, con puesto Cajero o Cocinero.

| Rol | Ruta | Qué hace |
|---|---|---|
| Cajero | `/login/` | Catálogo, ticket, matrícula del alumno, "Cobrar y Transmitir" y "Cancelar orden". Muestra alertas de incidencias. Los productos agotados aparecen bloqueados. |
| Cocinero | `/login/` | Lista de pedidos pendientes, "Listo para entregar", "Marcar como entregado", "Registrar incidencia" y control de disponibilidad de productos (Marcar agotado / Volver a disponible). |
| Estudiante | `/estado/` | Sin login. Consulta el estado de su pedido con su matrícula. |

Después de iniciar sesión, el sistema redirige según el puesto del empleado.

Para probar cajero y cocinero al mismo tiempo, usar dos sesiones separadas: una ventana normal y una de incógnito, o dos direcciones distintas (`http://127.0.0.1:8000/` y `http://localhost:8000/`). Un mismo navegador comparte la sesión entre pestañas.

## Casos de uso implementados

| Caso de uso | Descripción | Requisitos |
|---|---|---|
| CU-01 | Registrar pedido | RF-01, RF-02, RF-03 |
| CU-02 | Consultar órdenes pendientes | RF-04, RF-05 |
| CU-03 | Actualizar estado del pedido | RF-06, RF-07 |
| CU-04 | Consultar estado del pedido | RF-08 |
| CU-05 | Registrar incidencia y marcar productos agotados | RF-09 |

Validaciones y errores manejados: matrícula no registrada, ticket vacío, incidencia sin descripción, producto agotado (no se puede agregar al ticket ni cobrar) y restricción de pantallas por puesto.

## Estructura del código

- `config/`: configuración del proyecto y ruta técnica `/estado-bd/`.
- `alumnos/`, `catalogo/`, `empleados/`: modelos y administración de alumnos, productos (con el campo `disponible`) y empleados.
- `pedidos/`: modelos (Pedido, DetallePedido, Incidencia), vistas, rutas y plantillas de los casos de uso.

## Base de datos

Modelo de U2 implementado con migraciones de Django (alumnos, catalogo, empleados y pedidos). La BD se crea ejecutando `python manage.py migrate`. No se usa un script SQL aparte.

Ajustes respecto a U2: se agregó `matricula` en ALUMNO, `precio_aplicado` en DETALLE_PEDIDO y `disponible` en PRODUCTO; EMPLEADO se liga al usuario de autenticación de Django.

## Datos

Solo se usan datos ficticios. No se incluyen datos personales reales ni credenciales.