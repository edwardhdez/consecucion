from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ObjetivoSerializer, ConsecucionSerializer
from calculadora.models import Objetivo, Consecucion
from django.db.models import Max, Min
from rest_framework import status



@api_view(['GET'])
def apiOverview(request):

    api_urls = {
        'objetivos': '/objetivos/listar/',
        'consecuciones': '/listar/consecuciones/<str:pk>',
        'crear': '/crear/consecucion/',
        'calcular': 'calcular/consecucion/',
    }

    return Response(api_urls)


@api_view(['GET'])
def objetivosList(request):
    objetivos = Objetivo.objects.all()
    serializer = ObjetivoSerializer(objetivos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def objetivoDetail(request, pk):
    objetivo = Objetivo.objects.get(id=pk)
    serializer = ObjetivoSerializer(objetivo, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def consecucionesList(request, pk):
    objetivo = Objetivo.objects.get(id=pk)
    consecuciones = objetivo.consecucion_set.all()
    serializer = ConsecucionSerializer(consecuciones, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def crearObjetivo(request):
    objetivoSerializer = ObjetivoSerializer(data=request.data)
    if objetivoSerializer.is_valid():
        objetivoSerializer.save()
    return Response(objetivoSerializer.data)


@api_view(['PUT'])
def actualizarObjetivo(request, pk):
    objetivo = Objetivo.objects.get(id=pk)
    serializer = ObjetivoSerializer(instance=objetivo, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def crearConsecucion(request):
    consecucionSerializer = ConsecucionSerializer(data=request.data)
    if consecucionSerializer.is_valid():
        consecucionSerializer.save()
    return Response(consecucionSerializer.data)


@api_view(['DELETE'])
def eliminarConsecucion(request, pk):
    consecucion = Consecucion.objects.get(id=pk)
    consecucion.delete()
    return Response("Consecucion Eliminada: " + pk)


@api_view(['PUT'])
def actualizarConsecucion(request, pk):
    consecucion = Consecucion.objects.get(id=pk)
    serializer = ConsecucionSerializer(instance=consecucion, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def calcularConsecucion(request):
    objetivo = Objetivo.objects.get(id=request.data['objetivo'])
    cantidad = objetivo.consecucion_set.all().count()
    if cantidad < 2:
        return Response({'error': True,
                         'message': "Debe tener al menos 2 consecuciones definidas"})

    #filters = {
    #   'objetivo': request.data['objetivo'], 'meta': request.data['resultado']}
    consecucion = Consecucion.objects.filter(objetivo=request.data['objetivo'],
    meta=request.data['resultado']).first()

    if consecucion:
        return Response({'consecucion': consecucion.porcentaje})

    consecuciones_list = objetivo.consecucion_set.all().values_list('meta')
    minimo = consecuciones_list.order_by('meta').first()[0]
    maximo = consecuciones_list.order_by('meta').last()[0]
    resultado = float(request.data['resultado'])

    if objetivo.meta_ascendente:
        return metaAscendente(resultado, minimo, maximo)
    else:
        return metaDescendente(resultado, minimo, maximo)


def metaAscendente(resultado, minimo, maximo):
    if resultado < minimo:
        return Response({'consecucion': 0})
    elif resultado > maximo:
        return Response({'consecucion': 100})
    else:
        return Response({'error': True,
                         'message': "No se puede calcular el valor proporcionado. Verifique su tabla de consecuciones"})


def metaDescendente(resultado, minimo, maximo):
    if resultado > maximo:
        return Response({'consecucion': 0})
    elif resultado < minimo:
        return Response({'consecucion': 100})
    else:
        return Response({'error': True,
                         'message': "No se puede calcular el valor proporcionado. Verifique su tabla de consecuciones"})
