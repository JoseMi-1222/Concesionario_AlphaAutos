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
            ),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'})
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
        marca = cleaned.get('marca')
        modelo = cleaned.get('modelo')
        precio_max = cleaned.get('precio_max')

        # Si no hay ningún criterio: marcar cada campo con error para que se muestren en rojo
        if not any([v for v in (marca, modelo, precio_max) if v]):
            self.add_error('marca', 'Introduce al menos un criterio de búsqueda.')
            self.add_error('modelo', 'Introduce al menos un criterio de búsqueda.')
            self.add_error('precio_max', 'Introduce al menos un criterio de búsqueda.')
        else:
            # Validaciones adicionales
            if marca and len(marca.strip()) < 2:
                self.add_error('marca', 'Introduce al menos 2 caracteres para la marca.')
            if modelo and len(modelo.strip()) < 1:
                self.add_error('modelo', 'Introduce un modelo válido.')
            # Validación extra 1: precio máximo razonable
            if precio_max and precio_max > 10000000:
                self.add_error('precio_max', 'El precio máximo es excesivo para una búsqueda.')
            # Validación extra 2: caracteres válidos en modelo
            if modelo and any(not (c.isalnum() or c.isspace() or c in "-_.") for c in modelo):
                self.add_error('modelo', 'El modelo contiene caracteres inválidos.')

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
# Crud_Concesionario
# VISTA: Buscar un concesionario (CRUD - Create)
# -------------------------------------------------------------------
class ConcesionarioSearchForm(forms.Form):
    nombre = forms.CharField(required=False, label="Nombre")
    ciudad = forms.CharField(required=False, label="Ciudad")
    telefono = forms.CharField(required=False, label="Teléfono")

    def clean(self):
        cleaned = super().clean()
        nombre = cleaned.get('nombre')
        ciudad = cleaned.get('ciudad')
        telefono = cleaned.get('telefono')

        # Al menos un criterio: marcar campos cuando no hay ninguno
        if not any([v for v in (nombre, ciudad, telefono) if v]):
            self.add_error('nombre', 'Introduce al menos un criterio de búsqueda.')
            self.add_error('ciudad', 'Introduce al menos un criterio de búsqueda.')
            self.add_error('telefono', 'Introduce al menos un criterio de búsqueda.')
        else:
            # Validaciones adicionales
            if telefono and not telefono.isdigit():
                self.add_error('telefono', 'El teléfono debe contener solo números.')
            if nombre and len(nombre.strip()) < 2:
                self.add_error('nombre', 'Introduce al menos 2 caracteres para el nombre.')
            # Validación extra 1: la ciudad debe tener al menos 2 caracteres si se proporciona
            if ciudad and len(ciudad.strip()) < 2:
                self.add_error('ciudad', 'Introduce al menos 2 caracteres para la ciudad.')
            # Validación extra 2: teléfono razonable
            if telefono and len(telefono.strip()) < 7:
                self.add_error('telefono', 'El teléfono es demasiado corto para ser válido.')

        return cleaned
    
# -------------------------------------------------------------------
# Crud_Marca
# VISTA: Crear una nueva marca (CRUD - Create)
# -------------------------------------------------------------------

class MarcaModelForm(ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre', 'pais_origen', 'anio_fundacion', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }
        
    def clean(self):
        anio_fundacion = self.cleaned_data.get('anio_fundacion')
        descripcion = self.cleaned_data.get('descripcion')
        
        # Validar que el anio de fundación este dentro de un rango.
        current_year = datetime.now().year
        if anio_fundacion is not None and (anio_fundacion < 1950 or anio_fundacion > current_year):
            self.add_error('anio_fundacion', f'El anio de fundación debe estar entre 1950 y {current_year}.')
            
        # Validar que la descripción no tenga menos de 5 caracteres
        if descripcion is not None and len(descripcion) < 5:
            self.add_error('descripcion', 'La descripción debe tener al menos 5 caracteres.')
            
        return self.cleaned_data
    
# -------------------------------------------------------------------
# Crud_Marca
# VISTA: Buscar una marca (CRUD - Create)
# -------------------------------------------------------------------
class MarcaSearchForm(forms.Form):
    nombre = forms.CharField(required=False, label="Nombre")
    pais_origen = forms.CharField(required=False, label="País de Origen")
    anio_fundacion = forms.IntegerField(required=False, min_value=1900, max_value=datetime.now().year, label="anio de Fundación")

    def clean(self):
        cleaned = super().clean()
        nombre = cleaned.get('nombre')
        pais_origen = cleaned.get('pais_origen')
        anio_fundacion = cleaned.get('anio_fundacion')

        # Al menos un criterio
        if not any([v for v in (nombre, pais_origen, anio_fundacion) if v]):
            self.add_error('nombre', 'Introduce al menos un criterio de búsqueda.')
            self.add_error('pais_origen', 'Introduce al menos un criterio de búsqueda.')
            self.add_error('anio_fundacion', 'Introduce al menos un criterio de búsqueda.')
        else:
            # Validaciones adicionales
            if nombre and len(nombre.strip()) < 2:
                self.add_error('nombre', 'Introduce al menos 2 caracteres para el nombre.')
            if pais_origen and len(pais_origen.strip()) < 2:
                self.add_error('pais_origen', 'Introduce al menos 2 caracteres para el país de origen.')
            # Validación extra 1: nombre solo letras y espacios
            if nombre and not nombre.replace(' ', '').isalpha():
                self.add_error('nombre', 'El nombre de la marca solo debe contener letras.')
            # Validación extra 2: país sin dígitos
            if pais_origen and any(char.isdigit() for char in pais_origen):
                self.add_error('pais_origen', 'El país no debe contener números.')

        return cleaned
    
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
# Crud_Empleado
# VISTA: Buscar un empleado (CRUD - Create)
# -------------------------------------------------------------------
class EmpleadoSearchForm(forms.Form):
    nombre = forms.CharField(required=False, label="Nombre")
    puesto = forms.CharField(required=False, label="Puesto")
    concesionario = forms.ModelChoiceField(queryset=Concesionario.objects.all(), required=False, label="Concesionario")

    def clean(self):
        cleaned = super().clean()
        nombre = cleaned.get('nombre')
        puesto = cleaned.get('puesto')
        concesionario = cleaned.get('concesionario')

        # Al menos un criterio: marcar campos cuando no hay ninguno
        if not any([v for v in (nombre, puesto, concesionario) if v]):
            self.add_error('nombre', 'Introduce al menos un criterio de búsqueda.')
            self.add_error('puesto', 'Introduce al menos un criterio de búsqueda.')
            self.add_error('concesionario', 'Introduce al menos un criterio de búsqueda.')
        else:
            # Validaciones adicionales
            if nombre and len(nombre.strip()) < 2:
                self.add_error('nombre', 'Introduce al menos 2 caracteres para el nombre.')
            if puesto and len(puesto.strip()) < 2:
                self.add_error('puesto', 'Introduce al menos 2 caracteres para el puesto.')
            # Validación extra 1: el nombre no debe contener números
            if nombre and any(char.isdigit() for char in nombre):
                self.add_error('nombre', 'El nombre no puede contener números.')
            # Validación extra 2: límite razonable de longitud para puesto
            if puesto and len(puesto.strip()) > 50:
                self.add_error('puesto', 'El nombre del puesto es demasiado largo.')

        return cleaned
    
    
# -------------------------------------------------------------------
# Crud_Cliente
# VISTA: Crear un nuevo cliente (CRUD - Create)
# -------------------------------------------------------------------
class ClienteModelForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'fecha_registro']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'fecha_registro': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }
        
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
# Crud_Cliente
# VISTA: Buscar un cliente (CRUD - Create)
# -------------------------------------------------------------------
class ClienteSearchForm(forms.Form):
    nombre = forms.CharField(required=False, label="Nombre")
    email = forms.CharField(required=False, label="Email")
    telefono = forms.CharField(required=False, label="Teléfono")

    def clean(self):
        cleaned = super().clean()
        nombre = cleaned.get('nombre')
        email = cleaned.get('email')
        telefono = cleaned.get('telefono')

        # Al menos un criterio: marcar campos cuando no hay ninguno
        if not any([v for v in (nombre, email, telefono) if v]):
            self.add_error('nombre', 'Introduce al menos un criterio de búsqueda.')
            self.add_error('email', 'Introduce al menos un criterio de búsqueda.')
            self.add_error('telefono', 'Introduce al menos un criterio de búsqueda.')
        else:
            # Validaciones adicionales
            if email and '@' not in email:
                self.add_error('email', 'El email no tiene un formato válido.')
            if telefono and not telefono.isdigit():
                self.add_error('telefono', 'El teléfono debe contener solo números.')
            # Validación extra 1: nombre mínimo 2 caracteres
            if nombre and len(nombre.strip()) < 2:
                self.add_error('nombre', 'Introduce al menos 2 caracteres para el nombre.')
            # Validación extra 2: teléfono razonable
            if telefono and len(telefono.strip()) < 7:
                self.add_error('telefono', 'El teléfono es demasiado corto para ser válido.')

        return cleaned
    
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

# -------------------------------------------------------------------
# Crud_Aseguradora
# VISTA: Buscar una aseguradora (CRUD - Create)
# -------------------------------------------------------------------
class AseguradoraSearchForm(forms.Form):
    nombre = forms.CharField(required=False, label="Nombre")
    pais = forms.CharField(required=False, label="País")
    telefono = forms.CharField(required=False, label="Teléfono")

    def clean(self):
        cleaned = super().clean()
        nombre = cleaned.get('nombre')
        pais = cleaned.get('pais')
        telefono = cleaned.get('telefono')

        # Al menos un criterio: marcar campos cuando no hay ninguno
        if not any([v for v in (nombre, pais, telefono) if v]):
            self.add_error('nombre', 'Introduce al menos un criterio de búsqueda.')
            self.add_error('pais', 'Introduce al menos un criterio de búsqueda.')
            self.add_error('telefono', 'Introduce al menos un criterio de búsqueda.')
        else:
            # Validaciones adicionales
            if nombre and len(nombre.strip()) < 2:
                self.add_error('nombre', 'Introduce al menos 2 caracteres para el nombre.')
            if telefono and not telefono.isdigit():
                self.add_error('telefono', 'El teléfono debe contener solo números.')

        return cleaned

        
