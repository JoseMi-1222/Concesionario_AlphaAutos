# Concesionario_Django
Proyecto de un Concesionario en Django hecho por José Miguel Arras Gavira para la asignatura Desarrollo Web en Entorno Servidor.

# Proyecto AlphaAutos

## Descripción general

AlphaAutos es una aplicación Django para la gestión de un concesionario de automóviles.  
El sistema permite registrar concesionarios, empleados, clientes, coches, marcas, seguros, aseguradoras y mantenimientos.  
Se basa en un modelo entidad-relación de un concesionario real.

Se han definido 11 modelos con los siguientes requisitos:
- 3 relaciones OneToOne
- 3 relaciones ManyToOne
- 3 relaciones ManyToMany (una con tabla intermedia con atributos extra)
- Cada modelo tiene al menos 4 atributos
- Se utilizan más de 10 tipos distintos de campos y parámetros

---

## Modelos y explicaciones

### 1. Concesionario
Representa el concesionario principal.

**Atributos:**
- `nombre`: `CharField(max_length=100)`  
- `direccion`: `TextField()`  
- `telefono`: `CharField(max_length=20)`  
- `ciudad`: `CharField(max_length=50)`  

**Relaciones:**
- 1:N con `Empleado`  

---

### 2. Empleado
**Atributos:**
- `concesionario`: `ForeignKey(Concesionario, on_delete=models.CASCADE)`  
- `nombre`: `CharField(max_length=100)`  
- `puesto`: `CharField(max_length=100)`  
- `salario`: `DecimalField(max_digits=8, decimal_places=2)`  
- `fecha_contratacion`: `DateField()`  

**Relaciones:**
- ManyToOne con `Concesionario`  
- OneToOne con `UsuarioEmpleado`  

---

### 3. UsuarioEmpleado
**Atributos:**
- `empleado`: `OneToOneField(Empleado, on_delete=models.CASCADE)`  
- `direccion`: `TextField()`  
- `telefono`: `CharField(max_length=20)`  
- `experiencia`: `IntegerField(default=0)`  

**Relaciones:**
- OneToOne con `Empleado`  

---

### 4. Marca
**Atributos:**
- `nombre`: `CharField(max_length=50)`  
- `pais_origen`: `CharField(max_length=50)`  
- `año_fundacion`: `IntegerField(null=True)`  
- `descripcion`: `TextField(blank=True)`  

**Relaciones:**
- 1:N con `Coche`  

---

### 5. Coche
**Atributos:**
- `marca`: `ForeignKey(Marca, on_delete=models.CASCADE)`  
- `concesionario`: `ForeignKey(Concesionario, on_delete=models.CASCADE)`  
- `modelo`: `CharField(max_length=100)`  
- `precio`: `DecimalField(max_digits=10, decimal_places=2)`  
- `transmision`: `CharField(choices=TRANSMISIONES, default='MT', max_length=2)`  
- `fecha_fabricacion`: `DateField()`  

**Relaciones:**
- ManyToOne con `Marca` y `Concesionario`  
- ManyToMany con `Cliente` (a través de `Venta`)  
- ManyToMany con `Mantenimiento`  
- OneToOne con `Seguro`  

---

### 6. Cliente
**Atributos:**
- `nombre`: `CharField(max_length=100)`  
- `email`: `EmailField(unique=True)`  
- `telefono`: `CharField(max_length=20)`  
- `fecha_registro`: `DateTimeField(default=timezone.now)`  

**Relaciones:**
- OneToOne con `DatosCliente`  
- ManyToMany con `Coche` (a través de `Venta`)  

---

### 7. DatosCliente
**Atributos:**
- `cliente`: `OneToOneField(Cliente, on_delete=models.CASCADE)`  
- `direccion`: `TextField()`  
- `dni`: `CharField(max_length=15, unique=True)`  
- `puntos_fidelidad`: `FloatField(default=0.0)`  

**Relaciones:**
- OneToOne con `Cliente`  

---

### 8. Venta
**Atributos:**
- `cliente`: `ForeignKey(Cliente, on_delete=models.CASCADE)`  
- `coche`: `ForeignKey(Coche, on_delete=models.CASCADE)`  
- `fecha_venta`: `DateField(default=timezone.now)`  
- `precio_final`: `DecimalField(max_digits=10, decimal_places=2)`  
- `metodo_pago`: `CharField(max_length=50)`  

**Relaciones:**
- ManyToMany entre `Cliente` y `Coche` con tabla intermedia  

---

### 9. Seguro
**Atributos:**
- `coche`: `OneToOneField(Coche, on_delete=models.CASCADE)`  
- `tipo_seguro`: `CharField(max_length=50)`  
- `precio_mensual`: `DecimalField(max_digits=7, decimal_places=2)`  
- `duracion`: `IntegerField(help_text="Duración en meses")`  

**Relaciones:**
- OneToOne con `Coche`  
- ManyToMany con `Aseguradora`  

---

### 10. Aseguradora
**Atributos:**
- `nombre`: `CharField(max_length=100)`  
- `pais`: `CharField(max_length=50)`  
- `telefono`: `CharField(max_length=20)`  
- `web`: `URLField(blank=True)`  
- `seguros`: `ManyToManyField(Seguro)`  

**Relaciones:**
- ManyToMany con `Seguro`  

---

### 11. Mantenimiento
**Atributos:**
- `coches`: `ManyToManyField(Coche)`  
- `fecha_revision`: `DateField()`  
- `kilometros`: `IntegerField()`  
- `comentarios`: `TextField()`  
- `coste`: `DecimalField(max_digits=8, decimal_places=2)`  

**Relaciones:**
- ManyToMany con `Coche`  

---

## Tipos de campo y parámetros usados

**Tipos de campo:**
1. CharField  
2. TextField  
3. EmailField  
4. IntegerField  
5. FloatField  
6. DecimalField  
7. DateField  
8. DateTimeField  
9. URLField  
10. ForeignKey  
11. OneToOneField  
12. ManyToManyField  

**Parámetros comunes:**
- `max_length`: limita la longitud del texto.  
- `unique`: impide valores duplicados.  
- `default`: establece un valor por defecto.  
- `null`: permite valores nulos en la base de datos.  
- `blank`: permite dejar el campo vacío en formularios.  
- `choices`: define un conjunto de valores válidos.  
- `help_text`: muestra información adicional en el panel de administración.  
- `on_delete`: define el comportamiento al eliminar el objeto relacionado (por ejemplo, `models.CASCADE`).  

---

## URLs y vistas disponibles

| URL | Vista | Descripción |
|-----|------|-------------|
| `/` | `index` | Página de inicio con enlaces a todas las secciones. |
| `/coches/` | `coche_list` | Lista todos los coches con su marca y concesionario. |
| `/coche/<id_coche>/` | `coche_detail` | Muestra detalle de un coche concreto. |
| `/coches/<anio>/<mes>/` | `coches_por_fecha` | Lista coches fabricados en un año y mes concretos. |
| `/coches/transmision/<tipo>/` | `coches_transmision` | Filtra coches por tipo de transmisión. |
| `/concesionario/<id_concesionario>/coches/<texto>/` | `coches_concesionario_texto` | Muestra coches de un concesionario cuyo modelo contiene un texto. |
| `/coche/<id_coche>/ultimo_cliente/` | `ultimo_cliente_coche` | Muestra el último cliente que compró un coche. |
| `/coches/sin_ventas/` | `coches_sin_ventas` | Lista coches que no tienen ventas asociadas. |
| `/concesionario/<id_concesionario>/detalle/` | `concesionario_detail` | Muestra el concesionario con sus empleados y coches. |
| `/ventas/resumen/` | `resumen_ventas` | Calcula y muestra promedio, máximo y mínimo de precios de ventas. |
| `/concesionarios/` | `lista_concesionarios` | Lista todos los concesionarios registrados. |

---

## Templates y Requisitos funcionales implementados

1. **Gestión de concesionarios, empleados y coches**  
2. **Gestión de clientes y ventas**  
3. **Gestión de seguros y aseguradoras**  
4. **Gestión de mantenimientos**  
5. **Consultas agregadas con `aggregate()`**  
6. **Filtros y búsquedas por atributos**  
7. **Optimización de consultas (`select_related`, `prefetch_related`)**  
8. **Validaciones de datos (`unique`, `blank`, `null`)**  

---

## Uso de Template Tags, Filtros y Operadores

**Template Tags usadas:**
1. `{% if %} ... {% else %}` → en `coche_detail.html`, `ultimo_cliente_coche.html`.  
2. `{% for ... %} ... {% empty %}` → en `coche_list.html`, `coches_sin_ventas.html`, `concesionario_detail.html`.  
3. `{% include %}` → `for_row_coche.html` incluido en `coche_list.html` y `concesionario_detail.html`.  
4. `{% extends %}` → en todas las plantillas para heredar de `base.html`.  
5. `{% block %}` → en todas las plantillas para definir secciones como `title`, `cabecera`, `content`.  

## Operadores y Template Filters usados

### Operadores:
- `==` → para comprobar transmisión automática (`coche.transmision == 'AT'`)  
- `!=` → para marcas distintas (`coche.marca.nombre != 'Ford'`)  
- `>` → para precios altos (`coche.precio > 30000`)  
- `<` → para precios bajos (`coche.precio < 10000`)  
- `>=` → para ventas gama media-alta (`venta.precio_final >= 25000`)  

### Template Filters:
- `floatformat` → para mostrar precios con 2 decimales  (`coche_detail.html`)
- `upper` → para mostrar nombres en mayúsculas  (`coche_list.html`)
- `title` → para mostrar nombres y modelos capitalizados  (`base.html`) 
- `date` → para formatear fechas  (`coche_detail.html`)
- `length` → para contar elementos de listas (coches) (`concesionario_detail.html`)   

**Formato correcto de fechas:**  
- Todas las fechas se muestran con `|date:"d/m/Y"` en las plantillas (`coche_detail.html`, `coches_por_fecha.html`, `ultimo_cliente_coche.html`).  

---

## Widgets usados en los formularios

- **`forms.SelectDateWidget`**: usado en `AlphaAutos/form.py` para los campos **`fecha_fabricacion`** (en `CocheModelForm`) y **`fecha_contratacion`** (en `EmpleadoModelForm`). Proporciona selectores de día/mes/año.
- **`forms.NumberInput`**: usado en `AlphaAutos/form.py` para el campo **`precio`** (en `CocheModelForm`) — campo numérico con atributo `step` para decimales.
- **`forms.TextInput`**: usado en `AlphaAutos/form.py` para el campo **`modelo`** (en `CocheModelForm`) — input de texto simple.
- **`forms.Textarea`**: usado en `AlphaAutos/form.py` para el campo **`descripcion`** (en `MarcaModelForm`) — área de texto multipárrafo.
- **`forms.EmailInput`**: usado en `AlphaAutos/form.py` para el campo **`email`** (en `ClienteModelForm`) — input tipo email (valida formato en el navegador cuando procede).
- **`forms.DateInput`**: usado en `AlphaAutos/form.py` para el campo **`fecha_registro`** (en `ClienteModelForm`) — usa el selector de fecha nativo HTML5 (`type="date"`).

Estos widgets están definidos en `AlphaAutos/form.py` dentro de las clases `ModelForm` correspondientes. Si quieres que todos los campos usen estilos Bootstrap homogéneos o prefieres reemplazar `SelectDateWidget` por un `DateInput` con un datepicker JS, puedo hacer esos cambios también.

## Validaciones definidas en `AlphaAutos/form.py`

A continuación se listan todas las validaciones implementadas en `AlphaAutos/form.py`, indicando qué comprobación se hace y en qué formulario/campo se aplica.

- **`CocheModelForm.clean()`**
	- `precio` no puede ser nulo ni menor o igual a 0 → añade error en `precio` con mensaje: "El precio no puede ser negativo o 0." (formulario: `CocheModelForm`).
	- `fecha_fabricacion` no puede ser una fecha futura → añade error en `fecha_fabricacion` con mensaje: "La fecha de fabricación no puede ser futura." (formulario: `CocheModelForm`).

- **`CocheSearchForm`**
	- `precio_max` definido con `min_value=0` (campo): impide introducir valores negativos (validación de campo).
	- `clean()` ahora utiliza `cleaned = super().clean()` y **asocia errores a cada campo** usando `self.add_error(...)` cuando no se proporciona ningún criterio — esto hace que los campos se marquen como inválidos en las plantillas.
	- Validaciones adicionales añadidas (dos comprobaciones extra):
		- `marca`: mínimo 2 caracteres si se proporciona.
		- `modelo`: caracteres válidos únicamente (alfanuméricos, espacios, `- _ .`) y mínimo 1 carácter.
		- `precio_max`: límite razonable (se añade error si `> 10.000.000`).

- **`ConcesionarioModelForm.clean()`**
	- `nombre` no puede estar vacío → añade error en `nombre` con mensaje: "El nombre no puede estar vacío.".
	- `telefono` debe contener solo dígitos (si se proporciona) → añade error en `telefono` con mensaje: "El teléfono debe contener solo números.".

- **`ConcesionarioSearchForm.clean()`**
	- `clean()` usa `self.add_error(...)` por campo cuando no se proporciona ningún criterio de búsqueda (marcando los campos como inválidos en la UI).
	- Validaciones adicionales añadidas (dos comprobaciones extra):
		- `ciudad`: si se proporciona, mínimo 2 caracteres.
		- `telefono`: debe contener solo dígitos y, si se proporciona, mínimo 7 dígitos.

- **`MarcaModelForm.clean()`**
	- `año_fundacion` (si se proporciona) debe estar entre 1950 y el año actual → añade error en `año_fundacion` con mensaje: "El año de fundación debe estar entre 1950 y {current_year}.".
	- `descripcion` (si se proporciona) debe tener al menos 5 caracteres → añade error en `descripcion` con mensaje: "La descripción debe tener al menos 5 caracteres.".

- **`MarcaSearchForm`**
	- `anio_fundacion` definido con `min_value=1900` y `max_value=datetime.now().year` (validación de campo).
	- `clean()` ahora añade errores por campo con `self.add_error(...)` si no se proporcionan criterios de búsqueda.
	- Validaciones adicionales añadidas (dos comprobaciones extra):
		- `nombre`: mínimo 2 caracteres y solo letras/espacios (no permite números ni símbolos fuera de espacios).
		- `pais_origen`: mínimo 2 caracteres y no debe contener dígitos.

- **`EmpleadoModelForm.clean()`**
	- `salario` (si se proporciona) no puede ser menor o igual a 0 → añade error en `salario` con mensaje: "El salario no puede ser negativo o 0.".
	- `fecha_contratacion` no puede ser futura → añade error en `fecha_contratacion` con mensaje: "La fecha de contratación no puede ser futura.".

- **`EmpleadoSearchForm.clean()`**
	- `clean()` añade errores por campo vía `self.add_error(...)` cuando no hay criterios de búsqueda.
	- Validaciones adicionales añadidas (dos comprobaciones extra):
		- `nombre`: mínimo 2 caracteres y no debe contener números.
		- `puesto`: mínimo 2 caracteres y longitud máxima razonable (50 caracteres).

- **`ClienteModelForm.clean()`**
	- `email` (si se proporciona) se comprueba de forma simple: debe contener el carácter `@`; si no, añade error en `email` con mensaje: "El email no tiene un formato válido.".
	- `telefono` (si se proporciona) debe contener solo dígitos → añade error en `telefono` con mensaje: "El teléfono debe contener solo números.".

- **`ClienteSearchForm.clean()`**
	- `clean()` ahora asigna errores por campo con `self.add_error(...)` cuando no hay criterios de búsqueda.
	- Validaciones adicionales añadidas (dos comprobaciones extra):
		- `nombre`: mínimo 2 caracteres si se proporciona.
		- `telefono`: debe contener solo dígitos y, si se proporciona, mínimo 7 dígitos.

- **`AseguradoraModelForm.clean()`**
	- `telefono` (si se proporciona) debe contener solo dígitos → añade error en `telefono` con mensaje: "El teléfono debe contener solo números.".
	- `web` (si se proporciona) debe comenzar con `"www"` → añade error en `web` con mensaje: "La web debe comenzar con \"www\".".

- **`AseguradoraSearchForm.clean()`**
	- `clean()` usa `self.add_error(...)` por campo cuando no se proporciona ningún criterio de búsqueda.
	- Validaciones adicionales (ya presentes):
		- `nombre`: mínimo 2 caracteres si se proporciona.
		- `telefono`: debe contener solo dígitos si se proporciona.

Notas adicionales:
- Varias validaciones son comprobadas a nivel de campo usando parámetros de los campos (por ejemplo `min_value`, `max_value`) y no solo en `clean()`; estas comprobaciones aparecerán como errores de campo normales cuando se valide el formulario.

---

**Funcion para añadir imagenes**

- **`AlphaAutos/models.py` (modificado):** se añadió un campo para almacenar la imagen del `Coche` (p.ej. `ImageField`) para poder asociar fotos a cada vehículo.
- **`AlphaAutos/migrations/0004_coche_imagen.py` (añadida):** migración que crea el nuevo campo de imagen en la base de datos.
- **`AlphaAutos/form.py` (modificado):** los formularios de `Coche` se adaptaron para aceptar el campo de imagen en creación/edición.
- **`AlphaAutos/views.py` (modificado):** las vistas de crear/editar `Coche` añadieron manejo del archivo subido (guardar imagen) y el flujo de guardado se ajustó.
- **`AlphaAutos/urls.py` (modificado):** adaptaciones para servir archivos media en desarrollo o rutas relacionadas con imágenes (configuración de `MEDIA_URL`/`MEDIA_ROOT` en `mysite/settings.py`).
- **`mysite/settings.py` (modificado):** configuradas las variables `MEDIA_URL` y `MEDIA_ROOT` para servir y almacenar las imágenes subidas.
- **Plantillas (modificadas):**
	- `AlphaAutos/templates/Crud_Coche/crear_coche.html` — formulario actualizado para permitir subir imagen del coche.
	- `AlphaAutos/templates/Crud_Coche/editar_coche.html` — permite modificar la imagen asociada al coche.
	- `AlphaAutos/templates/concesionario/coche_detail.html` — muestra la imagen del coche en la vista de detalle y conserva el botón de editar.
- **Media (añadido):** `media/coches/*` — imágenes de ejemplo subidas al repositorio para pruebas (ej.: `3.jpg`, `ChatGPT_Image_...png`, etc.).

Cómo probar los cambios localmente:

- Asegúrate de tener instaladas las dependencias y el entorno activado.
- Ejecuta las migraciones para aplicar el nuevo campo:

```powershell
python manage.py migrate
```

- Levanta el servidor de desarrollo y verifica que `MEDIA_URL` esté servido (en dev Django lo hace automáticamente si está configurado):

```powershell
python manage.py runserver
```

- Ve a la página de creación/edición de coches, sube una imagen y comprueba en la vista de detalle que la imagen se muestra.

Notas:
- Si el servidor de producción gestiona archivos estáticos/media de forma distinta, configura `MEDIA_ROOT` y el servidor web (nginx, etc.) para servir las imágenes.
- Las imágenes incluidas en `media/coches/` son de ejemplo para desarrollo/testing; puedes eliminarlas o reemplazarlas según tus necesidades.



