from django.db import models
from django.utils import timezone


# Concesionario principal
class Concesionario(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


# Empleado (Muchos empleados pueden pertenecer a un concesionario)
class Empleado(models.Model):
    concesionario = models.ForeignKey(Concesionario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_contratacion = models.DateField()

    def __str__(self):
        return self.nombre


# Usuario_Empleado (1:1 con Empleado)
class Usuario_Empleado(models.Model):
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    experiencia = models.IntegerField(default=0)

    def __str__(self):
        return f"Usuario de {self.empleado.nombre}"


# Marca (1:N con Coches)
class Marca(models.Model):
    nombre = models.CharField(max_length=50)
    pais_origen = models.CharField(max_length=50)
    año_fundacion = models.IntegerField(null=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


# Coche (N:M con Cliente, N:M con Mantenimiento, 1:1 con Seguro)
class Coche(models.Model):
    TRANSMISIONES = [
        ('AT', 'Automática'),
        ('MT', 'Manual'),
    ]
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    concesionario = models.ForeignKey(Concesionario, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    transmision = models.CharField(max_length=2, choices=TRANSMISIONES, default='MT')
    fecha_fabricacion = models.DateField()

    def __str__(self):
        return f"{self.marca.nombre} {self.modelo}"


# Cliente (N:M con Coches)
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre


# Datos_Cliente (1:1 con Cliente)
class Datos_Cliente(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    direccion = models.TextField()
    dni = models.CharField(max_length=15, unique=True)
    puntos_fidelidad = models.FloatField(default=0.0)

    def __str__(self):
        return f"Datos de {self.cliente.nombre}"


# Venta (tabla intermedia N:M entre Cliente y Coche con atributos extras)
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE)
    fecha_venta = models.DateField(default=timezone.now)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"Venta de {self.coche} a {self.cliente.nombre}"


# Seguro (1:1 con Coche, N:M con Aseguradora)
class Seguro(models.Model):
    coche = models.OneToOneField(Coche, on_delete=models.CASCADE)
    tipo_seguro = models.CharField(max_length=50)
    precio_mensual = models.DecimalField(max_digits=7, decimal_places=2)
    duracion = models.IntegerField(help_text="Duración en meses")

    def __str__(self):
        return f"{self.tipo_seguro} - {self.coche.modelo}"


# Aseguradora (N:M con Seguro)
class Aseguradora(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    web = models.URLField(blank=True)
    seguros = models.ManyToManyField(Seguro)

    def __str__(self):
        return self.nombre


# Mantenimiento (N:M con Coches)
class Mantenimiento(models.Model):
    coches = models.ManyToManyField(Coche)
    fecha_revision = models.DateField()
    kilometros = models.IntegerField()
    comentarios = models.TextField()
    coste = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Mantenimiento general - {self.fecha_revision}"

