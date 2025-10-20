from django.urls import path, re_path
from . import views

app_name = "concesionario"

urlpatterns = [
    path('', views.index, name='index'),  # índice con acceso a todas las URLs
    path('concesionarios/', views.lista_concesionarios, name='lista_concesionarios'),  
]
