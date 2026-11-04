from django.http import HttpResponse

from alumnos.models import Alumno
from catalogo.models import Producto


def estado_bd(request):
    total_alumnos = Alumno.objects.count()
    total_productos = Producto.objects.count()
    return HttpResponse(
        f"Conexión a la BD correcta. Alumnos: {total_alumnos} | Productos: {total_productos}"
    )