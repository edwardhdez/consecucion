from django.db import models


class Objetivo(models.Model):
    descripcion = models.CharField(max_length=150, null=False)
    metrica = models.CharField(max_length=30, null=False)
    meta_ascendente = models.BooleanField(default=True)
    

    def __str__(self):
        return self.descripcion


class Consecucion(models.Model):
    descripcion = models.CharField(max_length=30, null=False)
    meta = models.FloatField()
    porcentaje = models.FloatField()
    objetivo = models.ForeignKey(
        Objetivo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.descripcion
