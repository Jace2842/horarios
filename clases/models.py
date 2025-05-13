from django.db import models
from django.contrib.auth.models import User

class Aula(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

class Clase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    numero_alumnos = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.nombre