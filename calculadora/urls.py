from django.urls import path
from . import views

urlpatterns = [
    path('consecuciones', views.calculadora, name="calculadora"),
    path('', views.objetivos, name="home"),

]
