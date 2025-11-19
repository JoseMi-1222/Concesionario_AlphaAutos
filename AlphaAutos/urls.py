from django.urls import path
from . import views

app_name = "AlphaAutos"

urlpatterns = [
    # Página inicial (Index)
    path('', views.index, name='index'),
    path('coches/', views.coche_list, name='coche_list'),
    path('coche/<int:id_coche>/', views.coche_detail, name='coche_detail'),
    path('coches/<int:anio>/<int:mes>/', views.coches_por_fecha, name='coches_por_fecha'),
    path('coches/transmision/<str:tipo>/', views.coches_transmision, name='coches_transmision'),
    path('concesionario/<int:id_concesionario>/coches/<str:texto>/', views.coches_concesionario_texto, name='coches_concesionario_texto'),
    path('coche/<int:id_coche>/ultimo_cliente/', views.ultimo_cliente_coche, name='ultimo_cliente_coche'),
    path('coches/sin_ventas/', views.coches_sin_ventas, name='coches_sin_ventas'),   
    path('concesionario/<int:id_concesionario>/detalle/', views.concesionario_detail, name='concesionario_detail'),
    path('ventas/resumen/', views.resumen_ventas, name='resumen_ventas'),
    path('concesionarios/', views.lista_concesionarios, name='lista_concesionarios'),
    path('coche/nuevo/', views.crear_coche, name='crear_coche'),

]
