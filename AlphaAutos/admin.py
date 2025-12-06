from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
admin.site.register(Usuario, UserAdmin)
admin.site.register(Gerente)
admin.site.register(Comprador)
admin.site.register(Concesionario)
admin.site.register(Empleado)
admin.site.register(Usuario_Empleado)
admin.site.register(Marca)
admin.site.register(Coche)
admin.site.register(Datos_Cliente)
admin.site.register(Venta)
admin.site.register(Seguro)
admin.site.register(Aseguradora)
admin.site.register(Mantenimiento)