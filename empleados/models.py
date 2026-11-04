from django.conf import settings
from django.db import models


class Empleado(models.Model):
    PUESTOS = [("Cajero", "Cajero"), ("Cocinero", "Cocinero")]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    puesto = models.CharField(max_length=20, choices=PUESTOS)

    def __str__(self):
        return f"{self.user.get_username()} ({self.puesto})"