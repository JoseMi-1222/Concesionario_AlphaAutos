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

]
