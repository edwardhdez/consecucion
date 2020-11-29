import json

from django.test import TestCase
from rest_framework.test import APIClient
from calculadora.models import Objetivo
from rest_framework import status
from collections import OrderedDict 

# Create your tests here.
class ConsecucionTestCase(TestCase):
    def setUp(self):
        Objetivo.objects.create(descripcion="Test A", metrica="Metrica A", meta_ascendente=True)
        Objetivo.objects.create(descripcion="Test B", metrica="Metrica B", meta_ascendente=False)
        Objetivo.objects.create(descripcion="Test C", metrica="Metrica C", meta_ascendente=True)

    def test_animals_can_speak(self):
        client = APIClient()
        response = client.get("/api/objetivos/listar")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals("Test A", response.data[0]['descripcion'])

        
