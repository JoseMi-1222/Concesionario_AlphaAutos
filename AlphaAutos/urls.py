from django.urls import path
from . import views

app_name = "AlphaAutos"

urlpatterns = [
    # Página inicial (Index)
    path('', views.index, name='index'),
]
