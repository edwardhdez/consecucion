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
        objetivoTest2 = Objetivo.objects.create(descripcion="Test B", metrica="Metrica B", meta_ascendente=True)

        Consecucion.objects.create(descripcion="Maxima",meta=7, porcentaje=80, objetivo=objetivoTest)
        Consecucion.objects.create(descripcion="Media", meta=6, porcentaje=90, objetivo=objetivoTest)
        Consecucion.objects.create(descripcion="Minimo",meta=5, porcentaje=100, objetivo=objetivoTest)

        Consecucion.objects.create(descripcion="Minimo",meta=5, porcentaje=80, objetivo=objetivoTest2)
        Consecucion.objects.create(descripcion="Media", meta=6, porcentaje=90, objetivo=objetivoTest2)
        Consecucion.objects.create(descripcion="Maximo", meta=7, porcentaje=100, objetivo=objetivoTest2)



    def test_objetivos_listar(self):
        client = APIClient()
        response = client.get("/api/objetivos/listar")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals("Test A", response.data[0]['descripcion'])

    def test_objetivo_detail(self):
        client = APIClient()
        response = client.get("/api/objetivo/1")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals("Test A",response.data['descripcion'])

    def test_objetivo_actualizar(self):
        client = APIClient()
        response = client.put("/api/objetivo/actualizar/1", {'descripcion': "Test A1", 'metrica': "Metrica A", 'meta_ascendente': False})
        print(response)
        self.assertEqual("Test A1",response.data['descripcion'])

    def test_consecuciones_listar(self):
        client = APIClient()
        response = client.get("/api/consecuciones/listar/1")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(3, len(response.data))

    def test_calcular_consecucion1(self):
        client = APIClient()
        data = {'objetivo': 1, 'resultado': 7}
        response = client.post("/api/consecucion/calcular", data)
        self.assertEqual(80, response.data['consecucion'])

    def test_calcular_consecucion2(self):
        client = APIClient()
        data = {'objetivo': 1, 'resultado': 6}
        response = client.post("/api/consecucion/calcular", data)
        self.assertEqual(90, response.data['consecucion'])

    def test_calcular_consecucion3(self):
        client = APIClient()
        data = {'objetivo': 1, 'resultado': 5}
        response = client.post("/api/consecucion/calcular", data)
        self.assertEqual(100, response.data['consecucion'])

    def test_calcular_consecucion4(self):
        client = APIClient()
        data = {'objetivo': 1, 'resultado': 3}
        response = client.post("/api/consecucion/calcular", data)
        self.assertEqual(100, response.data['consecucion'])
    
    def test_calcular_consecucion5(self):
        client = APIClient()
        data = {'objetivo': 1, 'resultado': 8}
        response = client.post("/api/consecucion/calcular", data)
        self.assertEqual(0, response.data['consecucion'])
    
    def test_calcular_consecucion6(self):
        client = APIClient()
        data = {'objetivo':2, 'resultado': 5}
        response = client.post("/api/consecucion/calcular", data)
        self.assertEqual(80, response.data['consecucion'])
    
    def test_calcular_consecucion7(self):
        client = APIClient()
        data = {'objetivo':2, 'resultado': 6}
        response = client.post("/api/consecucion/calcular", data)
        self.assertEqual(90, response.data['consecucion'])

    def test_calcular_consecucion7(self):
        client = APIClient()
        data = {'objetivo': 2, 'resultado': 7}
        response = client.post("/api/consecucion/calcular", data)
        self.assertEqual(100, response.data['consecucion'])

    def test_calcular_consecucion7(self):
        client = APIClient()
        data = {'objetivo': 2, 'resultado': 8}
        response = client.post("/api/consecucion/calcular", data)
        self.assertEqual(100, response.data['consecucion'])
    
    def test_calcular_consecucion7(self):
        client = APIClient()
        data = {'objetivo': 2, 'resultado': 3}
        response = client.post("/api/consecucion/calcular", data)
        self.assertEqual(0, response.data['consecucion'])
    
