from django.core.validators import MinValueValidator
from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True)
    precio = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)]
    )

    def __str__(self):
        return self.nombre