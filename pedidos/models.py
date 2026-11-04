from django.core.validators import MinValueValidator
from django.db import models


class Pedido(models.Model):
    ESTATUS = [
        ("Pendiente", "Pendiente"),
        ("Listo", "Listo"),
        ("Entregado", "Entregado"),
    ]

    fecha_hora = models.DateTimeField(auto_now_add=True)
    estatus = models.CharField(max_length=20, choices=ESTATUS, default="Pendiente")
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    alumno = models.ForeignKey("alumnos.Alumno", on_delete=models.PROTECT)
    empleado = models.ForeignKey("empleados.Empleado", on_delete=models.PROTECT)

    def __str__(self):
        return f"Pedido {self.id} - {self.estatus}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey("catalogo.Producto", on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_aplicado = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto}"


class Incidencia(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    fecha_reporte = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Incidencia del pedido {self.pedido_id}"