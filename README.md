# Concesionario_Django
# Proyecto de un Concesionario en Django hecho por José Miguel Arras Gavira para la asignatura Desarrollo Web en Entorno Servidor.

# Proyecto AlphaAutos

## Descripción general

AlphaAutos es una aplicación Django para la gestión de un concesionario de automóviles.  
El sistema permite registrar concesionarios, empleados, clientes, coches, marcas, seguros, aseguradoras y mantenimientos.  
Se basa en un modelo entidad-relación de un concesionario real.

Se han definido 10 modelos con los siguientes requisitos:
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
- `nombre`: `CharField(max_length=100)` → Nombre del concesionario. El parámetro `max_length` limita la longitud del texto.
- `direccion`: `TextField()` → Dirección completa sin límite de caracteres.
- `telefono`: `CharField(max_length=20)` → Número de teléfono de contacto.
- `ciudad`: `CharField(max_length=50)` → Ciudad donde se ubica el concesionario.

**Relaciones:**
- Relación 1:N con `Empleado` (un concesionario puede tener varios empleados).

---

### 2. Empleado
Representa a los trabajadores del concesionario.

**Atributos:**
- `concesionario`: `ForeignKey(Concesionario, on_delete=models.CASCADE)` → Relación con el concesionario.  
  El parámetro `on_delete=models.CASCADE` indica que si se elimina el concesionario, también se eliminarán sus empleados.
- `nombre`: `CharField(max_length=100)` → Nombre del empleado.
- `puesto`: `CharField(max_length=100)` → Cargo o rol dentro del concesionario.
- `salario`: `DecimalField(max_digits=8, decimal_places=2)` → Sueldo del empleado.  
  `max_digits` define el número total de dígitos y `decimal_places` los decimales.
- `fecha_contratacion`: `DateField()` → Fecha en la que fue contratado.

**Relaciones:**
- ManyToOne con `Concesionario`.
- OneToOne con `UsuarioEmpleado`.

---

### 3. UsuarioEmpleado
Datos adicionales del empleado (perfil interno).

**Atributos:**
- `empleado`: `OneToOneField(Empleado, on_delete=models.CASCADE)` → Relación uno a uno con un empleado.
- `direccion`: `TextField()` → Dirección del empleado.
- `telefono`: `CharField(max_length=20)` → Teléfono del empleado.
- `experiencia`: `IntegerField(default=0)` → Años de experiencia. El parámetro `default` establece un valor inicial.

**Relaciones:**
- OneToOne con `Empleado`.

---

### 4. Marca
Representa la marca de los vehículos.

**Atributos:**
- `nombre`: `CharField(max_length=50)` → Nombre de la marca.
- `pais_origen`: `CharField(max_length=50)` → País donde se fundó la marca.
- `año_fundacion`: `IntegerField(null=True)` → Año de fundación. `null=True` permite valores vacíos.
- `descripcion`: `TextField(blank=True)` → Descripción general. `blank=True` permite dejar el campo vacío en formularios.

**Relaciones:**
- OneToMany con `Coche`.

---

### 5. Coche
Modelo de automóvil disponible en el concesionario.

**Atributos:**
- `marca`: `ForeignKey(Marca, on_delete=models.CASCADE)` → Marca a la que pertenece.
- `concesionario`: `ForeignKey(Concesionario, on_delete=models.CASCADE)` → Concesionario donde se vende.
- `modelo`: `CharField(max_length=100)` → Modelo del coche.
- `precio`: `DecimalField(max_digits=10, decimal_places=2)` → Precio del coche.
- `transmision`: `CharField(choices=TRANSMISIONES, default='MT', max_length=2)` → Tipo de transmisión.  
  El parámetro `choices` define las opciones válidas y `default` el valor por defecto.
- `fecha_fabricacion`: `DateField()` → Fecha de fabricación.

**Relaciones:**
- ManyToOne con `Marca`.
- ManyToOne con `Concesionario`.
- ManyToMany con `Cliente` (a través de `Venta`).
- ManyToMany con `Mantenimiento`.
- OneToOne con `Seguro`.

---

### 6. Cliente
Representa a los clientes del concesionario.

**Atributos:**
- `nombre`: `CharField(max_length=100)` → Nombre completo.
- `email`: `EmailField(unique=True)` → Correo electrónico único. `unique=True` impide duplicados.
- `telefono`: `CharField(max_length=20)` → Teléfono de contacto.
- `fecha_registro`: `DateTimeField(default=timezone.now)` → Fecha y hora de registro. `default` usa la hora actual.

**Relaciones:**
- OneToOne con `DatosCliente`.
- ManyToMany con `Coche` (a través de `Venta`).

---

### 7. DatosCliente
Datos personales adicionales del cliente.

**Atributos:**
- `cliente`: `OneToOneField(Cliente, on_delete=models.CASCADE)` → Relación uno a uno con `Cliente`.
- `direccion`: `TextField()` → Dirección postal.
- `dni`: `CharField(max_length=15, unique=True)` → Documento nacional de identidad. `unique=True` evita duplicados.
- `puntos_fidelidad`: `FloatField(default=0.0)` → Puntos acumulados por compras.

**Relaciones:**
- OneToOne con `Cliente`.

---

### 8. Venta
Tabla intermedia que representa una venta entre Cliente y Coche con información adicional.

**Atributos:**
- `cliente`: `ForeignKey(Cliente, on_delete=models.CASCADE)` → Cliente que realiza la compra.
- `coche`: `ForeignKey(Coche, on_delete=models.CASCADE)` → Coche vendido.
- `fecha_venta`: `DateField(default=timezone.now)` → Fecha en la que se realiza la venta.
- `precio_final`: `DecimalField(max_digits=10, decimal_places=2)` → Precio final del coche.
- `metodo_pago`: `CharField(max_length=50)` → Método de pago utilizado.

**Relaciones:**
- ManyToMany entre `Cliente` y `Coche` (con tabla intermedia).

---

### 9. Seguro
Asociado a un coche y a varias aseguradoras.

**Atributos:**
- `coche`: `OneToOneField(Coche, on_delete=models.CASCADE)` → Coche asegurado.
- `tipo_seguro`: `CharField(max_length=50)` → Tipo de seguro (básico, completo, etc.).
- `precio_mensual`: `DecimalField(max_digits=7, decimal_places=2)` → Precio mensual del seguro.
- `duracion`: `IntegerField(help_text="Duración en meses")` → Duración del seguro en meses.  
  `help_text` muestra una descripción en el panel de administración.

**Relaciones:**
- OneToOne con `Coche`.
- ManyToMany con `Aseguradora`.

---

### 10. Aseguradora
Compañías de seguros asociadas a los coches.

**Atributos:**
- `nombre`: `CharField(max_length=100)` → Nombre de la aseguradora.
- `pais`: `CharField(max_length=50)` → País donde opera.
- `telefono`: `CharField(max_length=20)` → Teléfono de contacto.
- `web`: `URLField(blank=True)` → Página web. `blank=True` permite dejarlo vacío.
- `seguros`: `ManyToManyField(Seguro)` → Seguros que ofrece la compañía.

**Relaciones:**
- ManyToMany con `Seguro`.

---

### 11. Mantenimiento
Registro de revisiones o reparaciones de coches.

**Atributos:**
- `coches`: `ManyToManyField(Coche)` → Coches implicados en el mantenimiento.
- `fecha_revision`: `DateField()` → Fecha de la revisión.
- `kilometros`: `IntegerField()` → Kilómetros recorridos al momento de la revisión.
- `comentarios`: `TextField()` → Observaciones o detalles de la revisión.
- `coste`: `DecimalField(max_digits=8, decimal_places=2)` → Costo total del mantenimiento.

**Relaciones:**
- ManyToMany con `Coche`.

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