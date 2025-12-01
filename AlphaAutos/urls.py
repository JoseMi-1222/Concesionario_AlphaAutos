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
    path('marcas/', views.lista_marcas, name='lista_marcas'),
    path('coche/nuevo/', views.crear_coche, name='crear_coche'),
    path('concesionario/nuevo/', views.crear_concesionario, name='crear_concesionario'),
    path('marca/nuevo/', views.crear_marca, name='crear_marca'),
    path('marca/<int:id_marca>/', views.marca_detail, name='marca_detail'),
    path('marca/editar/<int:id_marca>/', views.editar_marca, name='editar_marca'),
    path('empleados/', views.lista_empleados, name='lista_empleados'),
    path('empleado/nuevo/', views.crear_empleado, name='crear_empleados'),
    path('empleado/<int:id_empleado>/', views.empleado_detail, name='empleado_detail'),
    path('empleado/editar/<int:id_empleado>/', views.editar_empleado, name='editar_empleado'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('cliente/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('cliente/<int:id_cliente>/', views.cliente_detail, name='cliente_detail'),
    path('cliente/editar/<int:id_cliente>/', views.editar_cliente, name='editar_cliente'),
    path('aseguradoras/', views.lista_aseguradoras, name='lista_aseguradoras'),
    path('aseguradora/nuevo/', views.crear_aseguradora, name='crear_aseguradora'),
    path('aseguradora/<int:id_aseguradora>/', views.aseguradora_detail, name='aseguradora_detail'),
    path('aseguradora/editar/<int:id_aseguradora>/', views.editar_aseguradora, name='editar_aseguradora'),
    path('buscar_coches/', views.buscar_coches, name='buscar_coches'),
    path('buscar_concesionarios/', views.buscar_concesionarios, name='buscar_concesionarios'),
    path('buscar_marcas/', views.buscar_marcas, name='buscar_marcas'),
    path('buscar_empleados/', views.buscar_empleados, name='buscar_empleados'),
    path('buscar_clientes/', views.buscar_clientes, name='buscar_clientes'),
    path('buscar_aseguradoras/', views.buscar_aseguradoras, name='buscar_aseguradoras'),
    path('coche/editar/<int:id_coche>/', views.editar_coche, name='editar_coche'),
    path('concesionario/editar/<int:id_concesionario>/', views.editar_concesionario, name='editar_concesionario'),
    path('coche/eliminar/<int:id_coche>/', views.eliminar_coche, name='eliminar_coche'),
    path('concesionario/eliminar/<int:id_concesionario>/', views.eliminar_concesionario, name='eliminar_concesionario'),
    path('marca/eliminar/<int:id_marca>/', views.eliminar_marca, name='eliminar_marca'),
    path('empleado/eliminar/<int:id_empleado>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('cliente/eliminar/<int:id_cliente>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('aseguradora/eliminar/<int:id_aseguradora>/', views.eliminar_aseguradora, name='eliminar_aseguradora'),
]

# Añadir configuración para servir archivos de medios en modo desarrollo
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)