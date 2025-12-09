from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, Avg, Max, Min, Count, Sum
from django.contrib.auth.hashers import make_password
from datetime import datetime
from .models import *
from .form import *
import AlphaAutos.form as form_module 
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout

# -------------------------------
# VISTA: Errores
# -------------------------------
def mi_error_404(request, exception=None):
    return render(request, "errores/404.html", status=404)

def mi_error_500(request):
    return render(request, "errores/500.html", status=500)

def mi_error_403(request, exception=None):
    return render(request, "errores/403.html", status=403)

def mi_error_400(request, exception=None):
    return render(request, "errores/400.html", status=400)

# -------------------------------
# VISTA: Página inicial (Index)
# -------------------------------
def index(request):
    # VARIABLE SESIÓN 1: Fecha inicio (Global)
    if "fecha_inicio" not in request.session:
        request.session["fecha_inicio"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # LÓGICA SOLO PARA USUARIOS LOGUEADOS (Variables de sesión extra)
    if request.user.is_authenticated:
        # VARIABLE SESIÓN 2: ID del usuario
        if "id_usuario" not in request.session:
            request.session["id_usuario"] = request.user.id
            
        # VARIABLE SESIÓN 3: Rol en texto
        if "rol_texto" not in request.session:
            request.session["rol_texto"] = request.user.get_rol_display()
            
        # VARIABLE SESIÓN 4: Contador de visitas a la Home
        request.session["visitas_home"] = request.session.get("visitas_home", 0) + 1

    return render(request, 'concesionario/index.html')

# --------------------------------------------------
# VISTA: Listar todos los coches (Requiere Login)
# --------------------------------------------------
@login_required
def coche_list(request):
    coches = Coche.objects.select_related('marca', 'concesionario').order_by('marca__nombre')
    contexto = {'coches': coches}
    return render(request, 'concesionario/coche_list.html', contexto)

# ------------------------------------------------------------
# VISTA: Detalle Coche (Requiere Login)
# ------------------------------------------------------------
@login_required
def coche_detail(request, id_coche):
    coche = get_object_or_404(
        Coche.objects.select_related('marca', 'concesionario'),
        id=id_coche
    )
    contexto = {'coche': coche}
    return render(request, 'concesionario/coche_detail.html', contexto)

# ----------------------------------------------------------------
# VISTA: Coches por fecha (Requiere Login)
# ----------------------------------------------------------------
@login_required
def coches_por_fecha(request, anio, mes):
    coches = Coche.objects.filter(
        fecha_fabricacion__year=anio,
        fecha_fabricacion__month=mes
    ).select_related('marca', 'concesionario').order_by('-fecha_fabricacion')

    contexto = {'coches': coches, 'anio': anio, 'mes': mes}
    return render(request, 'concesionario/coches_por_fecha.html', contexto)

# -----------------------------------------------------------------
# VISTA: Coches por transmisión (Requiere Login)
# -----------------------------------------------------------------
@login_required
def coches_transmision(request, tipo):
    coches = Coche.objects.filter(
        Q(transmision=tipo) | Q(transmision='MT')
    ).select_related('marca', 'concesionario').order_by('marca__nombre')

    contexto = {'coches': coches, 'tipo': tipo}
    return render(request, 'concesionario/coches_transmision.html', contexto)

# -------------------------------------------------------------------
# VISTA: Coches por concesionario y texto (Requiere Login)
# -------------------------------------------------------------------
@login_required
def coches_concesionario_texto(request, id_concesionario, texto):
    coches = Coche.objects.filter(
        concesionario_id=id_concesionario,
        modelo__icontains=texto
    ).select_related('marca', 'concesionario').order_by('marca__nombre')

    concesionario = Concesionario.objects.get(id=id_concesionario)
    contexto = {'coches': coches, 'texto': texto, 'concesionario': concesionario}
    return render(request, 'concesionario/coches_concesionario_texto.html', contexto)

# -------------------------------------------------------------------
# VISTA: Último cliente de un coche (Requiere Login)
# -------------------------------------------------------------------
@login_required
def ultimo_cliente_coche(request, id_coche):
    ultima_venta = Venta.objects.filter(coche_id=id_coche).order_by('-fecha_venta').first()
    ultimo_cliente = ultima_venta.comprador if ultima_venta else None # Corregido a .comprador según modelo

    contexto = {'venta': ultima_venta, 'ultimo_cliente': ultimo_cliente}
    return render(request, 'concesionario/ultimo_cliente_coche.html', contexto)

# --------------------------------------------------------------------
# VISTA: Coches sin ventas (Requiere Login)
# --------------------------------------------------------------------
@login_required
def coches_sin_ventas(request):
    coches = Coche.objects.filter(venta__isnull=True).select_related('marca', 'concesionario').order_by('marca__nombre')
    contexto = {'coches': coches}
    return render(request, 'concesionario/coches_sin_ventas.html', contexto)

# -------------------------------------------------------------------
# VISTA: Detalle Concesionario (Requiere Login)
# -------------------------------------------------------------------
@login_required
def concesionario_detail(request, id_concesionario):
    concesionario = get_object_or_404(Concesionario, id=id_concesionario)
    empleados = concesionario.empleado_set.all()
    coches = concesionario.coche_set.select_related('marca').all()

    contexto = {'concesionario': concesionario, 'empleados': empleados, 'coches': coches}
    return render(request, 'concesionario/concesionario_detail.html', contexto)

# -------------------------------------------------------------------
# VISTA: Resumen Ventas (Requiere Login)
# -------------------------------------------------------------------
@login_required
def resumen_ventas(request):
    resumen = Venta.objects.aggregate(
        total_ventas=Count('id'),
        suma_importes=Sum('precio_final'),
        precio_medio=Avg('precio_final'),
        precio_max=Max('precio_final'),
        precio_min=Min('precio_final')
    )
    return render(request, 'concesionario/resumen_ventas.html', {'resumen': resumen})

# -------------------------------------------------------------------
# VISTA: Listas Generales (Requiere Login)
# -------------------------------------------------------------------
@login_required
def lista_concesionarios(request):
    concesionarios = Concesionario.objects.all()
    return render(request, 'concesionario/lista_concesionario.html', {'concesionarios': concesionarios})

@login_required
def lista_marcas(request):
    marcas = Marca.objects.all()
    return render(request, 'concesionario/lista_marcas.html', {'marcas': marcas})

@login_required
def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'concesionario/lista_empleados.html', {'empleados': empleados})

@login_required
def lista_clientes(request):
    clientes = Comprador.objects.select_related('usuario').all()
    return render(request, 'concesionario/lista_clientes.html', {'clientes': clientes})

@login_required
def lista_aseguradoras(request):
    aseguradoras = Aseguradora.objects.all()
    return render(request, 'concesionario/lista_aseguradoras.html', {'aseguradoras': aseguradoras})

# ===================================================================
# GESTIÓN DE COCHES (CRUD)
# ===================================================================

@permission_required('AlphaAutos.add_coche')
def crear_coche(request):
    if request.method == 'POST':
        form = CocheModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Coche creado correctamente.")
            return redirect('AlphaAutos:coche_list')
    else:
        form = CocheModelForm()
    return render(request, 'Crud_Coche/crear_coche.html', {'form': form})

@permission_required('AlphaAutos.change_coche')
def editar_coche(request, id_coche):
    coche = get_object_or_404(Coche, id=id_coche)
    if request.method == 'POST':
        formulario = CocheModelForm(request.POST, request.FILES, instance=coche)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "Coche editado correctamente.")
                return redirect('AlphaAutos:coche_detail', id_coche=coche.id)
            except Exception as e:
                messages.error(request, f"Error al guardar: {e}")
    else:
        formulario = CocheModelForm(instance=coche)
    return render(request, 'Crud_Coche/editar_coche.html', {'formulario': formulario, 'coche': coche})

@permission_required('AlphaAutos.delete_coche')
def eliminar_coche(request, id_coche):
    coche = get_object_or_404(Coche, id=id_coche)
    try:
        coche.delete()
        messages.success(request, "Coche eliminado correctamente.")
    except:
        pass
    return redirect('AlphaAutos:coche_list')

@login_required
def buscar_coches(request):
    form = CocheSearchForm(request.GET or None)
    if len(request.GET) > 0 and form.is_valid():
        qs = Coche.objects.all()
        marca = form.cleaned_data.get("marca")
        modelo = form.cleaned_data.get("modelo")
        precio_max = form.cleaned_data.get("precio_max")
        if marca: qs = qs.filter(marca__nombre__icontains=marca)
        if modelo: qs = qs.filter(modelo__icontains=modelo)
        if precio_max: qs = qs.filter(precio__lte=precio_max)
        return render(request, "Crud_Coche/coche_busqueda.html", {"form": form, "coches": qs.all() })
    return render(request, "Crud_Coche/buscar_coches.html", {"form": form})

# ===================================================================
# GESTIÓN DE CONCESIONARIOS (CRUD)
# ===================================================================

@permission_required('AlphaAutos.add_concesionario')
def crear_concesionario(request):
    if request.method == 'POST':
        form = ConcesionarioModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Concesionario creado correctamente.")
            return redirect('AlphaAutos:lista_concesionarios')
    else:
        form = ConcesionarioModelForm()
    return render(request, 'Crud_Concesionario/crear_concesionario.html', {'form': form})

@permission_required('AlphaAutos.change_concesionario')
def editar_concesionario(request, id_concesionario):
    concesionario = get_object_or_404(Concesionario, id=id_concesionario)
    if request.method == 'POST':
        formulario = ConcesionarioModelForm(request.POST, instance=concesionario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Concesionario editado.")
            return redirect('AlphaAutos:concesionario_detail', id_concesionario=concesionario.id)
    else:
        formulario = ConcesionarioModelForm(instance=concesionario)
    return render(request, 'Crud_Concesionario/editar_concesionario.html', {'formulario': formulario, 'concesionario': concesionario})

@permission_required('AlphaAutos.delete_concesionario')
def eliminar_concesionario(request, id_concesionario):
    concesionario = get_object_or_404(Concesionario, id=id_concesionario)
    concesionario.delete()
    messages.success(request, "Concesionario eliminado.")
    return redirect('AlphaAutos:lista_concesionarios')

@login_required
def buscar_concesionarios(request):
    form = ConcesionarioSearchForm(request.GET or None)
    if len(request.GET) > 0 and form.is_valid():
        qs = Concesionario.objects.all()
        nombre = form.cleaned_data.get("nombre")
        ciudad = form.cleaned_data.get("ciudad")
        telefono = form.cleaned_data.get("telefono")
        if nombre: qs = qs.filter(nombre__icontains=nombre)
        if ciudad: qs = qs.filter(ciudad__icontains=ciudad)
        if telefono: qs = qs.filter(telefono__icontains=telefono)
        return render(request, "Crud_Concesionario/concesionario_busqueda.html", {"form": form, "concesionarios": qs.all()})
    return render(request, "Crud_Concesionario/buscar_concesionarios.html", {"form": form})

# ===================================================================
# GESTIÓN DE MARCAS (CRUD)
# ===================================================================

@permission_required('AlphaAutos.add_marca')
def crear_marca(request):
    if request.method == 'POST':
        form = MarcaModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Marca creada.")
            return redirect('AlphaAutos:lista_marcas')
    else:
        form = MarcaModelForm()
    return render(request, 'Crud_Marca/crear_marca.html', {'form': form})

@permission_required('AlphaAutos.change_marca')
def editar_marca(request, id_marca):
    marca = get_object_or_404(Marca, id=id_marca)
    if request.method == 'POST':
        formulario = MarcaModelForm(request.POST, instance=marca)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Marca editada.")
            return redirect('AlphaAutos:lista_marcas')
    else:
        formulario = MarcaModelForm(instance=marca)
    return render(request, 'Crud_Marca/editar_marca.html', {'formulario': formulario, 'marca': marca})

@permission_required('AlphaAutos.delete_marca')
def eliminar_marca(request, id_marca):
    marca = get_object_or_404(Marca, id=id_marca)
    marca.delete()
    messages.success(request, "Marca eliminada.")
    return redirect('AlphaAutos:lista_marcas')

@login_required
def marca_detail(request, id_marca):
    marca = get_object_or_404(Marca, id=id_marca)
    coches = marca.coche_set.select_related('concesionario').all()
    return render(request, 'concesionario/marca_detail.html', {'marca': marca, 'coches': coches})

@login_required
def buscar_marcas(request):
    form = MarcaSearchForm(request.GET or None)
    if len(request.GET) > 0 and form.is_valid():
        qs = Marca.objects.all()
        nombre = form.cleaned_data.get("nombre")
        pais = form.cleaned_data.get("pais_origen")
        anio = form.cleaned_data.get("anio_fundacion")
        if nombre: qs = qs.filter(nombre__icontains=nombre)
        if pais: qs = qs.filter(pais_origen__icontains=pais)
        if anio: qs = qs.filter(anio_fundacion=anio)
        return render(request, "Crud_Marca/marca_busqueda.html", {"form": form, "marcas": qs.all()})
    return render(request, "Crud_Marca/buscar_marcas.html", {"form": form})

# ===================================================================
# GESTIÓN DE EMPLEADOS (CRUD)
# ===================================================================

@permission_required('AlphaAutos.add_empleado')
def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado creado.")
            return redirect('AlphaAutos:lista_empleados')
    else:
        form = EmpleadoModelForm()
    return render(request, 'Crud_Empleados/crear_empleados.html', {'form': form})

@permission_required('AlphaAutos.change_empleado')
def editar_empleado(request, id_empleado):
    empleado = get_object_or_404(Empleado, id=id_empleado)
    if request.method == 'POST':
        formulario = EmpleadoModelForm(request.POST, instance=empleado)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Empleado editado.")
            return redirect('AlphaAutos:lista_empleados')
    else:
        formulario = EmpleadoModelForm(instance=empleado)
    return render(request, 'Crud_Empleados/editar_empleados.html', {'formulario': formulario, 'empleado': empleado})

@permission_required('AlphaAutos.delete_empleado')
def eliminar_empleado(request, id_empleado):
    empleado = get_object_or_404(Empleado, id=id_empleado)
    empleado.delete()
    messages.success(request, "Empleado eliminado.")
    return redirect('AlphaAutos:lista_empleados')

@login_required
def empleado_detail(request, id_empleado):
    empleado = get_object_or_404(Empleado, id=id_empleado)
    return render(request, 'concesionario/empleado_detail.html', {'empleado': empleado})

@login_required
def buscar_empleados(request):
    form = EmpleadoSearchForm(request.GET or None)
    if len(request.GET) > 0 and form.is_valid():
        qs = Empleado.objects.all()
        nombre = form.cleaned_data.get("nombre")
        puesto = form.cleaned_data.get("puesto")
        concesionario = form.cleaned_data.get("concesionario")
        if nombre: qs = qs.filter(nombre__icontains=nombre)
        if puesto: qs = qs.filter(puesto__icontains=puesto)
        if concesionario: qs = qs.filter(concesionario=concesionario)
        return render(request, "Crud_Empleados/empleado_busqueda.html", {"form": form, "empleados": qs.all()})
    return render(request, "Crud_Empleados/buscar_empleados.html", {"form": form})

# ===================================================================
# GESTIÓN DE CLIENTES / COMPRADORES (CRUD)
# ===================================================================

@permission_required('AlphaAutos.add_comprador')
def crear_cliente(request):
    if request.method == 'POST':
        form = CompradorModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente creado.")
            return redirect('AlphaAutos:lista_clientes')
    else:
        form = CompradorModelForm()
    return render(request, 'Crud_Clientes/crear_cliente.html', {'form': form})

@permission_required('AlphaAutos.change_comprador')
def editar_cliente(request, id_cliente):
    comprador = get_object_or_404(Comprador, id=id_cliente)
    # Importación local para evitar dependencias circulares si las hubiera
    from .form import CompradorEditForm 
    if request.method == 'POST':
        formulario = CompradorEditForm(request.POST, instance=comprador)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Cliente editado.")
            return redirect('AlphaAutos:lista_clientes')
    else:
        formulario = CompradorEditForm(instance=comprador)
    return render(request, 'Crud_Clientes/editar_cliente.html', {'formulario': formulario, 'cliente': comprador})

@permission_required('AlphaAutos.delete_comprador')
def eliminar_cliente(request, id_cliente):
    comprador = get_object_or_404(Comprador, id=id_cliente)
    comprador.delete()
    messages.success(request, "Cliente eliminado.")
    return redirect('AlphaAutos:lista_clientes')

@login_required
def cliente_detail(request, id_cliente):
    cliente = get_object_or_404(Comprador, id=id_cliente)
    return render(request, 'concesionario/cliente_detail.html', {'cliente': cliente})

@login_required
def buscar_clientes(request):
    form = CompradorSearchForm(request.GET or None)
    if len(request.GET) > 0 and form.is_valid():
        qs = Comprador.objects.select_related('usuario').all()
        usuario = form.cleaned_data.get("usuario")
        if usuario: qs = qs.filter(usuario__username__icontains=usuario)
        return render(request, "Crud_Clientes/cliente_busqueda.html", {"form": form, "clientes": qs.all()})
    return render(request, "Crud_Clientes/buscar_clientes.html", {"form": form})

@permission_required('AlphaAutos.change_comprador')
def cambiar_password_cliente(request, id_cliente):
    comprador = get_object_or_404(Comprador, id=id_cliente)
    from .form import CambiarPasswordForm
    if request.method == 'POST':
        formulario = CambiarPasswordForm(request.POST)
        if formulario.is_valid():
            password = formulario.cleaned_data['password1']
            comprador.usuario.password = make_password(password)
            comprador.usuario.save()
            messages.success(request, 'Contraseña cambiada.')
            return redirect('AlphaAutos:lista_clientes') # Redirigimos a lista, no login
    else:
        formulario = CambiarPasswordForm()
    return render(request, 'Crud_Clientes/cambiar_password_cliente.html', {'formulario': formulario, 'cliente': comprador})

# ===================================================================
# GESTIÓN DE ASEGURADORAS (CRUD)
# ===================================================================

@permission_required('AlphaAutos.add_aseguradora')
def crear_aseguradora(request):
    if request.method == 'POST':
        form = AseguradoraModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Aseguradora creada.")
            return redirect('AlphaAutos:lista_aseguradoras')
    else:
        form = AseguradoraModelForm()
    return render(request, 'Crud_Aseguradora/crear_aseguradora.html', {'form': form})

@permission_required('AlphaAutos.change_aseguradora')
def editar_aseguradora(request, id_aseguradora):
    aseguradora = get_object_or_404(Aseguradora, id=id_aseguradora)
    if request.method == 'POST':
        formulario = AseguradoraModelForm(request.POST, instance=aseguradora)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Aseguradora editada.")
            return redirect('AlphaAutos:lista_aseguradoras')
    else:
        formulario = AseguradoraModelForm(instance=aseguradora)
    return render(request, 'Crud_Aseguradora/editar_aseguradora.html', {'formulario': formulario, 'aseguradora': aseguradora})

@permission_required('AlphaAutos.delete_aseguradora')
def eliminar_aseguradora(request, id_aseguradora):
    aseguradora = get_object_or_404(Aseguradora, id=id_aseguradora)
    aseguradora.delete()
    messages.success(request, "Aseguradora eliminada.")
    return redirect('AlphaAutos:lista_aseguradoras')

@login_required
def aseguradora_detail(request, id_aseguradora):
    aseguradora = get_object_or_404(Aseguradora, id=id_aseguradora)
    return render(request, 'concesionario/aseguradora_detail.html', {'aseguradora': aseguradora})

@login_required
def buscar_aseguradoras(request):
    form = AseguradoraSearchForm(request.GET or None)
    if len(request.GET) > 0 and form.is_valid():
        qs = Aseguradora.objects.all()
        nombre = form.cleaned_data.get("nombre")
        pais = form.cleaned_data.get("pais")
        telefono = form.cleaned_data.get("telefono")
        if nombre: qs = qs.filter(nombre__icontains=nombre)
        if pais: qs = qs.filter(pais__icontains=pais)
        if telefono: qs = qs.filter(telefono__icontains=telefono)
        return render(request, "Crud_Aseguradora/aseguradora_busqueda.html", {"form": form, "aseguradoras": qs.all()})
    return render(request, "Crud_Aseguradora/buscar_aseguradoras.html", {"form": form})

# ===================================================================
# GESTIÓN DE VENTAS (CRUD)
# ===================================================================

@login_required
def lista_ventas(request):
    qs = Venta.objects.select_related('coche', 'comprador').all()
    
    # REQUISITO: Búsqueda Filtrada por Usuario
    # Si soy Comprador (Rol 3), solo veo mis compras
    if request.user.is_authenticated and request.user.rol == Usuario.COMPRADOR:
        qs = qs.filter(comprador__usuario=request.user)
        
    return render(request, 'concesionario/lista_ventas.html', {'ventas': qs})

@login_required
def venta_detail(request, id_venta):
    venta = get_object_or_404(Venta, id=id_venta)
    return render(request, 'concesionario/venta_detail.html', {'venta': venta})

@permission_required('AlphaAutos.add_venta')
def crear_venta(request):
    if request.method == 'POST':
        # IMPORTANTE: Pasamos user=request.user al formulario
        form = VentaModelForm(request.POST, request=request.user)
        
        if form.is_valid():
            venta = form.save(commit=False)
            
            # Asignar precio automático
            venta.precio_final = venta.coche.precio 
            
            # Asignar comprador automático (porque el campo ya no está en el form)
            if request.user.rol == Usuario.COMPRADOR:
                venta.comprador = request.user.comprador
            
            venta.save()
            messages.success(request, f"Venta creada correctamente por {venta.precio_final} €.")
            return redirect('AlphaAutos:lista_ventas')
    else:
        #También pasamos el usuario aquí para que se oculte el campo al entrar
        form = VentaModelForm(request=request.user)
    
    return render(request, 'Crud_Venta/crear_venta.html', {'form': form})


@permission_required('AlphaAutos.change_venta')
def editar_venta(request, id_venta):
    venta = get_object_or_404(Venta, id=id_venta)
    if request.method == 'POST':
        form = VentaModelForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            messages.success(request, "Venta editada.")
            return redirect('AlphaAutos:lista_ventas')
    else:
        form = VentaModelForm(instance=venta)
    return render(request, 'Crud_Venta/editar_venta.html', {'form': form, 'venta': venta})

@permission_required('AlphaAutos.delete_venta')
def eliminar_venta(request, id_venta):
    venta = get_object_or_404(Venta, id=id_venta)
    venta.delete()
    messages.success(request, "Venta eliminada.")
    return redirect('AlphaAutos:lista_ventas')

@login_required
@login_required
def buscar_ventas(request):
    # 1. Pasamos 'user=request.user' al formulario
    form = VentaSearchForm(request.GET or None, request=request.user)
    qs = Venta.objects.select_related('coche', 'comprador').all()

    # 2. FILTRO DE SEGURIDAD: Si es Comprador, SOLO ve sus ventas (Backend)
    if request.user.rol == Usuario.COMPRADOR:
        qs = qs.filter(comprador__usuario=request.user)

    # 3. Lógica de búsqueda del formulario
    if len(request.GET) > 0 and form.is_valid():
        coche = form.cleaned_data.get("coche")
        pago = form.cleaned_data.get("metodo_pago")
        
        # Solo intentamos filtrar por comprador si el campo existe (es decir, si NO es comprador)
        comprador = form.cleaned_data.get("comprador")
        
        if coche: 
            qs = qs.filter(coche__modelo__icontains=coche)
        
        if pago: 
            qs = qs.filter(metodo_pago__icontains=pago)
            
        # Solo aplicamos este filtro si el usuario es Gerente/Admin (porque el Comprador no ve este campo)
        if comprador and request.user.rol != Usuario.COMPRADOR:
            qs = qs.filter(comprador__usuario__username__icontains=comprador)

        return render(request, "Crud_Venta/venta_busqueda.html", {"form": form, "ventas": qs.all()})
        
    return render(request, "Crud_Venta/buscar_ventas.html", {"form": form})

# -------------------------------------------------------------------
# Registro de Usuario (Público)
# -------------------------------------------------------------------
def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            telefono = formulario.cleaned_data.get('telefono')
            
            if rol == Usuario.COMPRADOR:
                grupo = Group.objects.get(name='Compradores')
                user.groups.add(grupo)
                Comprador.objects.create(usuario=user, telefono=telefono)
            elif rol == Usuario.GERENTE:
                grupo = Group.objects.get(name='Gerentes')
                user.groups.add(grupo)
                Gerente.objects.create(usuario=user)
            
            messages.success(request, "Registrado correctamente.")
            login(request, user)
            return redirect('AlphaAutos:index')
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})

# ---------------------------------------------------
# VISTAS PERSONALIZADAS PARA CONTRASEÑAS
# ---------------------------------------------------

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'concesionario/registration/password_change_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # 1. Guardamos la nueva contraseña
        form.save()
        
        # 2. CERRAMOS LA SESIÓN (Logout) explícitamente
        logout(self.request)
        
        # 3. Mandamos el mensaje y redirigimos
        messages.success(self.request, "Tu contraseña ha sido cambiada correctamente. Por favor, inicia sesión de nuevo.")
        return redirect(self.success_url)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'concesionario/registration/password_reset_confirm.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # 1. Guarda la nueva contraseña explícitamente
        form.save()
        
        # 2. Mensaje y redirección al login
        messages.success(self.request, "Contraseña restablecida correctamente. Ya puedes iniciar sesión.")
        return redirect(self.success_url)