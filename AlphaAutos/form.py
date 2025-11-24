from datetime import datetime
from django import forms
from .models import *
from django.forms import ModelForm
 
class CocheModelForm(ModelForm):
    class Meta:
        model = Coche
        current_year = datetime.now().year
        fields = ['marca', 'concesionario', 'modelo', 'precio', 'transmision', 'fecha_fabricacion']
        widgets = {
             'fecha_fabricacion': forms.SelectDateWidget(
                years=range(current_year - 10, current_year + 11),
                attrs={'class': 'form-select d-inline w-auto'}
            )
        }
        
    def clean(self):
        precio = self.cleaned_data.get('precio')
        fecha_fabricacion = self.cleaned_data.get('fecha_fabricacion')
        
        # Validar que el precio no sea negativo
        if precio is not None and precio <= 0:
            self.add_error('precio', 'El precio no puede ser negativo o 0.')
            
        # Validar que la fecha de fabricación no sea futura
        if fecha_fabricacion is not None and fecha_fabricacion > datetime.now().date():
            self.add_error('fecha_fabricacion', 'La fecha de fabricación no puede ser futura.')
        return self.cleaned_data
        



        
