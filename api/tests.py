import json

from django.test import TestCase
from rest_framework.test import APIClient
from calculadora.models import Objetivo , Consecucion
from rest_framework import status
from collections import OrderedDict 

# Create your tests here.
class ConsecucionTestCase(TestCase):
    def setUp(self):
        objetivoTest = Objetivo.objects.create(descripcion="Test A", metrica="Metrica A", meta_ascendente=False)
        Objetivo.objects.create(descripcion="Test B", metrica="Metrica B", meta_ascendente=True)
        Objetivo.objects.create(descripcion="Test C", metrica="Metrica C", meta_ascendente=True)
        Consecucion.objects.create(descripcion="Maxima",meta=7, porcentaje=80.00, objetivo=objetivoTest)
        Consecucion.objects.create(descripcion="Media", meta=6, porcentaje=90, objetivo=objetivoTest)
        Consecucion.objects.create(descripcion="Minimo",meta=5, porcentaje=100, objetivo=objetivoTest)

    def test_objetivos_listar(self):
        client = APIClient()
        response = client.get("/api/objetivos/listar")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals("Test A", response.data[0]['descripcion'])

        
