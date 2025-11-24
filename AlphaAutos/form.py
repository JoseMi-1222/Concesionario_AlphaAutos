from datetime import datetime
from django import forms
from .models import *
from django.forms import ModelForm

# -------------------------------------------------------------------
# Crud_Coche
# VISTA: Crear un nuevo coche (CRUD - Create)
# -------------------------------------------------------------------
 
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
    
# -------------------------------------------------------------------
# Crud_Concesionario
# VISTA: Crear un nuevo concesionario (CRUD - Create)
# -------------------------------------------------------------------

class ConcesionarioModelForm(ModelForm):
    class Meta:
        model = Concesionario
        fields = ['nombre', 'direccion', 'telefono', 'ciudad']
        
    def clean(self):
        nombre = self.cleaned_data.get('nombre')
        telefono = self.cleaned_data.get('telefono')
        
        # Validar que el nombre no esté vacío
        if not nombre:
            self.add_error('nombre', 'El nombre no puede estar vacío.')
            
        # Validar que el teléfono tenga un formato adecuado (ejemplo simple)
        if telefono and not telefono.isdigit():
            self.add_error('telefono', 'El teléfono debe contener solo números.')
            
        return self.cleaned_data
    
# -------------------------------------------------------------------
# Crud_Marca
# VISTA: Crear una nueva marca (CRUD - Create)
# -------------------------------------------------------------------

class MarcaModelForm(ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre', 'pais_origen', 'año_fundacion', 'descripcion']
        
    def clean(self):
        año_fundacion = self.cleaned_data.get('año_fundacion')
        descripcion = self.cleaned_data.get('descripcion')
        
        # Validar que el año de fundación este dentro de un rango.
        current_year = datetime.now().year
        if año_fundacion is not None and (año_fundacion < 1950 or año_fundacion > current_year):
            self.add_error('año_fundacion', f'El año de fundación debe estar entre 1950 y {current_year}.')
            
        # Validar que la descripción no tenga menos de 5 caracteres
        if descripcion is not None and len(descripcion) < 5:
            self.add_error('descripcion', 'La descripción debe tener al menos 5 caracteres.')
            
        return self.cleaned_data



        
