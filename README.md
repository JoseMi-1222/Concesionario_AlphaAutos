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

---

## Requisitos funcionales implementados

1. **Gestión de concesionarios, empleados y coches**  
2. **Gestión de clientes y ventas**  
3. **Gestión de seguros y aseguradoras**  
4. **Gestión de mantenimientos**  
5. **Consultas agregadas con `aggregate()`**  
6. **Filtros y búsquedas por atributos**  
7. **Optimización de consultas (`select_related`, `prefetch_related`)**  
8. **Validaciones de datos (`unique`, `blank`, `null`)**  