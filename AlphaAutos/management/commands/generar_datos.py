from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from AlphaAutos.models import *

fake = Faker('es_ES')

class Command(BaseCommand):
    help = 'Genera datos de prueba para todos los modelos del concesionario AlphaAutos'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Creando datos de prueba...'))

        # Crear Concesionarios
        concesionarios = []
        for _ in range(10):
            c = Concesionario.objects.create(
                nombre=f"Concesionario {fake.company()}",
                direccion=fake.address(),
                telefono=fake.phone_number(),
                ciudad=fake.city()
            )
            concesionarios.append(c)

        # Crear Marcas
        marcas = []
        for _ in range(10):
            m = Marca.objects.create(
                nombre=fake.company(),
                pais_origen=fake.country(),
                año_fundacion=random.randint(1950, 2020),
                descripcion=fake.text(100)
            )
            marcas.append(m)

        # Crear Coches
        coches = []
        for _ in range(10):
            c = Coche.objects.create(
                marca=random.choice(marcas),
                concesionario=random.choice(concesionarios),
                modelo=fake.word().capitalize(),
                precio=round(random.uniform(8000, 60000), 2),
                transmision=random.choice(['MT', 'AT']),
                fecha_fabricacion=fake.date_between(start_date='-5y', end_date='today')
            )
            coches.append(c)

        # Crear Clientes
        clientes = []
        for _ in range(10):
            cl = Cliente.objects.create(
                nombre=fake.name(),
                email=fake.unique.email(),
                telefono=fake.phone_number(),
                fecha_registro=timezone.now()
            )
            clientes.append(cl)

        # Crear DatosCliente (OneToOne con Cliente)
        for cliente in clientes:
            Datos_Cliente.objects.create(
                cliente=cliente,
                direccion=fake.address(),
                dni=fake.unique.bothify(text='########A'),
                puntos_fidelidad=random.uniform(0, 100)
            )

        # Crear Empleados
        empleados = []
        for _ in range(10):
            e = Empleado.objects.create(
                concesionario=random.choice(concesionarios),
                nombre=fake.name(),
                puesto=random.choice(['Vendedor', 'Mecánico', 'Gerente', 'Administrativo']),
                salario=round(random.uniform(1200, 3000), 2),
                fecha_contratacion=fake.date_between(start_date='-10y', end_date='today')
            )
            empleados.append(e)

        # Crear UsuarioEmpleado (OneToOne con Empleado)
        for empleado in empleados:
            Usuario_Empleado.objects.create(
                empleado=empleado,
                direccion=fake.address(),
                telefono=fake.phone_number(),
                experiencia=random.randint(0, 20)
            )

        # Crear Aseguradoras
        aseguradoras = []
        for _ in range(10):
            a = Aseguradora.objects.create(
                nombre=fake.company(),
                pais=fake.country(),
                telefono=fake.phone_number(),
                web=fake.url()
            )
            aseguradoras.append(a)

        # Crear Seguros (OneToOne con Coche)
        seguros = []
        for coche in coches:
            s = Seguro.objects.create(
                coche=coche,
                tipo_seguro=random.choice(['Básico', 'Completo', 'Premium']),
                precio_mensual=round(random.uniform(30, 200), 2),
                duracion=random.randint(6, 36)
            )
            s.aseguradora_set.add(random.choice(aseguradoras))
            seguros.append(s)

        # Crear Mantenimientos
        mantenimientos = []
        for _ in range(10):
            m = Mantenimiento.objects.create(
                fecha_revision=fake.date_between(start_date='-2y', end_date='today'),
                kilometros=random.randint(5000, 120000),
                comentarios=fake.sentence(),
                coste=round(random.uniform(100, 1000), 2)
            )
            # Añadimos coches aleatorios
            m.coches.add(random.choice(coches))
            mantenimientos.append(m)

        # Crear Ventas (ManyToMany con tabla intermedia)
        for _ in range(10):
            Venta.objects.create(
                cliente=random.choice(clientes),
                coche=random.choice(coches),
                fecha_venta=fake.date_between(start_date='-2y', end_date='today'),
                precio_final=round(random.uniform(9000, 50000), 2),
                metodo_pago=random.choice(['Transferencia', 'Efectivo', 'Financiación'])
            )

        self.stdout.write(self.style.SUCCESS('Datos de prueba creados correctamente.'))
