from django.shortcuts import render
import requests


def objetivos(request):
    base_url = request.build_absolute_uri('/')
    # api/objetivos/listar
    objetivos = requests.get(f'{base_url}api/objetivos/listar').json()
    context = {
        'objetivos': objetivos
    }

    return render(request, 'calculadora/objetivos.html', context)


def calculadora(request):
    id_objetivo = request.GET['objetivo']
    base_url = request.build_absolute_uri('/')
    objetivo = requests.get(f'{base_url}api/objetivo/{id_objetivo}').json()
    consecuciones = requests.get(
        f'{base_url}api/consecuciones/listar/{id_objetivo}').json()
    context = {
        'objetivo': objetivo,
        'consecuciones': consecuciones
    }
    return render(request, 'calculadora/calculadora.html', context)
