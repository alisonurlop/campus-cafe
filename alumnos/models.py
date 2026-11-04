from django.db import models


class Alumno(models.Model):
    matricula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.matricula} - {self.nombre}"