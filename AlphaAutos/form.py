from django import forms
from .models import *
from django.forms import ModelForm
 
class CocheModelForm(ModelForm):
    class Meta:
        model = Coche
        fields = ['marca', 'concesionario', 'modelo', 'precio', 'transmision', 'fecha_fabricacion']
        labels = {
            "modelo": ("Modelo del coche")
        }
        help_texts = {
            "modelo" : ("100 caracteres como maximo")
        }
        widgets = {
            "fecha_fabricacion":forms.SelectDateWidget()
        }
        localized_fields = ["fecha_fabricacion"]