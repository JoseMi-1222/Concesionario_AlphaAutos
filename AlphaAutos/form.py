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
# Crud_Coche
# VISTA: Buscar un coche (CRUD - Read)
# -------------------------------------------------------------------
class CocheSearchForm(forms.Form):
    marca = forms.CharField(required=False, label="Marca")
    modelo = forms.CharField(required=False, label="Modelo")
    precio_max = forms.DecimalField(required=False, min_value=0, label="Precio Máximo")

    def clean(self):
        cleaned = super().clean()
        if not any(cleaned.values()):
            raise forms.ValidationError("Introduce al menos un criterio de búsqueda.")
        return cleaned

    
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
    
# -------------------------------------------------------------------
# Crud_Empleado
# VISTA: Crear un nuevo empleado (CRUD - Create)
# -------------------------------------------------------------------
class EmpleadoModelForm(ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'puesto', 'fecha_contratacion', 'concesionario', 'salario']
        widgets = {
             'fecha_contratacion': forms.SelectDateWidget(
                years=range(2000, datetime.now().year + 10),
                attrs={'class': 'form-select d-inline w-auto'}
            )
        }
        
    def clean(self):
        salario = self.cleaned_data.get('salario')
        fecha_contratacion = self.cleaned_data.get('fecha_contratacion')
        
        # Validar que el salario no sea negativo ni 0
        if salario is not None and salario <= 0:
            self.add_error('salario', 'El salario no puede ser negativo o 0.')
    
        # Validar que la fecha de contratación no sea futura
        if fecha_contratacion is not None and fecha_contratacion > datetime.now().date():
            self.add_error('fecha_contratacion', 'La fecha de contratación no puede ser futura.')
            
        return self.cleaned_data
    
# -------------------------------------------------------------------
# Crud_Cliente
# VISTA: Crear un nuevo cliente (CRUD - Create)
# -------------------------------------------------------------------
class ClienteModelForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'fecha_registro']
        
    def clean(self):
        email = self.cleaned_data.get('email')
        telefono = self.cleaned_data.get('telefono')
        
        # Validar que el email tenga un formato adecuado (ejemplo simple)
        if email and "@" not in email:
            self.add_error('email', 'El email no tiene un formato válido.')
            
        # Validar que el teléfono tenga un formato adecuado (ejemplo simple)
        if telefono and not telefono.isdigit():
            self.add_error('telefono', 'El teléfono debe contener solo números.')
            
        return self.cleaned_data
    
# -------------------------------------------------------------------
# Crud_Aseguradora
# VISTA: Crear una nueva aseguradora (CRUD - Create)
# -------------------------------------------------------------------
class AseguradoraModelForm(ModelForm):
    class Meta:
        model = Aseguradora
        fields = ['nombre', 'pais', 'telefono', 'web', 'seguros']
        
    def clean(self):
        telefono = self.cleaned_data.get('telefono')
        web = self.cleaned_data.get('web')
            
        # Validar que el teléfono tenga un formato adecuado (ejemplo simple)
        if telefono and not telefono.isdigit():
            self.add_error('telefono', 'El teléfono debe contener solo números.')
            
        # Validar que la web tenga un formato adecuado (ejemplo simple)
        if web and not web.startswith("www"):
            self.add_error('web', 'La web debe comenzar con "www".')
            
        return self.cleaned_data



        
