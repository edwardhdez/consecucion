from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.apiOverview, name="api_overview"),
    path('api/objetivos/listar', views.objetivosList, name="objetivos"),
    path('api/objetivo/<str:pk>', views.objetivoDetail, name="objetivo"),
    path('api/objetivo/crear', views.crearObjetivo, name = "objetivo_crear"),
    path('api/objetivo/actualizar/<str:pk>',views.actualizarObjetivo, name="objetivo_actualizar"),
    path('api/consecuciones/listar/<str:pk>',views.consecucionesList, name="consecuciones"),
    path('api/consecucion/crear', views.crearConsecucion ,name="consecucion_crear"),
    path('api/consecucion/actualizar/<str:pk>', views.actualizarConsecucion, name="consecucion_actualizar"),
    path('api/consecucion/eliminar/<str:pk>', views.eliminarConsecucion, name="consecucion_eliminar"),
    path('api/consecucion/calcular', views.calcularConsecucion, name="consecucion_calcular"),

]
