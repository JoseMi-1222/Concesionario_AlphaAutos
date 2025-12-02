from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from django.db.models import F, Q, Avg, Max, Min, Count, Sum
from .form import *

# -------------------------------
# VISTA: Errores
# -------------------------------

def mi_error_404(request, exception=None):
    return render(request, "errores/404.html", None, None, 404) 

def mi_error_500(request):
    return render(request, "errores/500.html", None, None, 500)

def mi_error_403(request, exception=None):
    return render(request, "errores/403.html", None, None, 403)

def mi_error_400(request, exception=None):
    return render(request, "errores/400.html", None, None, 400) 

# -------------------------------
# VISTA: Página inicial (Index)
# -------------------------------
def index(request):
    if(not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        
    return render(request, 'concesionario/index.html')

# --------------------------------------------------
# VISTA: Listar todos los coches con sus relaciones
# --------------------------------------------------
def coche_list(request):
    coches = Coche.objects.select_related('marca', 'concesionario').order_by('marca__nombre')
    contexto = {'coches': coches}
    return render(request, 'concesionario/coche_list.html', contexto)

# ------------------------------------------------------------
# VISTA: Mostrar un coche concreto mediante su id (int)
# ------------------------------------------------------------
def coche_detail(request, id_coche):
    coche = get_object_or_404(
        Coche.objects.select_related('marca', 'concesionario'),
        id=id_coche
    )
    contexto = {'coche': coche}
    return render(request, 'concesionario/coche_detail.html', contexto)

# ----------------------------------------------------------------
# VISTA: Listar coches fabricados en un anio y mes concretos
# ----------------------------------------------------------------
def coches_por_fecha(request, anio, mes):
    coches = Coche.objects.filter(
        fecha_fabricacion__year=anio,
        fecha_fabricacion__month=mes
    ).select_related('marca', 'concesionario').order_by('-fecha_fabricacion')

    contexto = {
        'coches': coches,
        'anio': anio,
        'mes': mes,
    }
    return render(request, 'concesionario/coches_por_fecha.html', contexto)

# -----------------------------------------------------------------
# VISTA: Filtrar coches por tipo de transmisión (filtro con OR)
# -----------------------------------------------------------------
def coches_transmision(request, tipo):
    coches = Coche.objects.filter(
        Q(transmision=tipo) | Q(transmision='MT')
    ).select_related('marca', 'concesionario').order_by('marca__nombre')

    contexto = {
        'coches': coches,
        'tipo': tipo,
    }
    return render(request, 'concesionario/coches_transmision.html', contexto)

# -------------------------------------------------------------------
# VISTA: Coches de un concesionario cuyo modelo contiene un texto
# -------------------------------------------------------------------
def coches_concesionario_texto(request, id_concesionario, texto):
    coches = Coche.objects.filter(
        concesionario_id=id_concesionario,
        modelo__icontains=texto
    ).select_related('marca', 'concesionario').order_by('marca__nombre')

    concesionario = Concesionario.objects.get(id=id_concesionario)

    contexto = {
        'coches': coches,
        'texto': texto,
        'concesionario': concesionario,
    }
    return render(request, 'concesionario/coches_concesionario_texto.html', contexto)


# -------------------------------------------------------------------
# VISTA: Mostrar el último cliente que compró un coche (tabla intermedia)
# -------------------------------------------------------------------
def ultimo_cliente_coche(request, id_coche):
    ultima_venta = Venta.objects.filter(coche_id=id_coche).order_by('-fecha_venta').first()
    ultimo_cliente = ultima_venta.cliente if ultima_venta else None

    contexto = {
        'venta': ultima_venta,
        'ultimo_cliente': ultimo_cliente
    }
    return render(request, 'concesionario/ultimo_cliente_coche.html', contexto)


# --------------------------------------------------------------------
# VISTA: Mostrar coches que no tienen ventas (isnull=True)
# --------------------------------------------------------------------
def coches_sin_ventas(request):
    coches = Coche.objects.filter(venta__isnull=True).select_related('marca', 'concesionario').order_by('marca__nombre')
    contexto = {'coches': coches}
    return render(request, 'concesionario/coches_sin_ventas.html', contexto)

# -------------------------------------------------------------------
# VISTA: Mostrar un concesionario y sus relaciones (empleados, coches)
# -------------------------------------------------------------------
def concesionario_detail(request, id_concesionario):
    concesionario = get_object_or_404(Concesionario, id=id_concesionario)
    empleados = concesionario.empleado_set.all()
    coches = concesionario.coche_set.select_related('marca').all()

    contexto = {
        'concesionario': concesionario,
        'empleados': empleados,
        'coches': coches,
    }
    return render(request, 'concesionario/concesionario_detail.html', contexto)

# -------------------------------------------------------------------
# VISTA: Calcula el promedio, máximo y mínimo de los precios de ventas.
# -------------------------------------------------------------------
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
# VISTA: Listar todos los concesionarios
# -------------------------------------------------------------------
def lista_concesionarios(request):
    concesionarios = Concesionario.objects.all()  # Obtiene todos los concesionarios
    context = {'concesionarios': concesionarios}
    return render(request, 'concesionario/lista_concesionario.html', context)

# -------------------------------------------------------------------
# VISTA: Listar todas las marcas
# -------------------------------------------------------------------
def lista_marcas(request):
    marcas = Marca.objects.all()  # Obtiene todas las marcas
    context = {'marcas': marcas}
    return render(request, 'concesionario/lista_marcas.html', context)

# -------------------------------------------------------------------
# VISTA: Listar todos los empleados
# -------------------------------------------------------------------
def lista_empleados(request):
    empleados = Empleado.objects.all()  # Obtiene todos los empleados
    context = {'empleados': empleados}
    return render(request, 'concesionario/lista_empleados.html', context) 

# -------------------------------------------------------------------
# VISTA: Listar todos los clientes
# -------------------------------------------------------------------
def lista_clientes(request):
    clientes = Cliente.objects.all()  # Obtiene todos los clientes
    context = {'clientes': clientes}
    return render(request, 'concesionario/lista_clientes.html', context)

# -------------------------------------------------------------------
# Vista: Listar todas las aseguradoras
# -------------------------------------------------------------------
def lista_aseguradoras(request):
    aseguradoras = Aseguradora.objects.all()  # Obtiene todas las aseguradoras
    context = {'aseguradoras': aseguradoras}
    return render(request, 'concesionario/lista_aseguradoras.html', context)

# -------------------------------------------------------------------
# Vista: Formulario para crear un nuevo coche
# -------------------------------------------------------------------
def crear_coche(request):
    if request.method == 'POST':
        form = CocheModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Coche creado correctamente.")
            return redirect('AlphaAutos:coche_list')
    else:
        form = CocheModelForm()
    
    contexto = {'form': form}
    return render(request, 'Crud_Coche/crear_coche.html', contexto)

# -------------------------------------------------------------------
# Vista: Formulario para buscar un coche
# -------------------------------------------------------------------
def buscar_coches(request):
    form = CocheSearchForm(request.GET or None)

    if(len(request.GET)>0):
        if form.is_valid():
            qs = Coche.objects
            marca = form.cleaned_data.get("marca")
            modelo = form.cleaned_data.get("modelo")
            precio_max = form.cleaned_data.get("precio_max")
            if marca:
                qs = qs.filter(marca__nombre__icontains=marca)
            if modelo:
                qs = qs.filter(modelo__icontains=modelo)
            if precio_max is not None:
                qs = qs.filter(precio__lte=precio_max)


            coches = qs.all()
            contexto = {"form": form, "coches": coches}

            #Renderizar los resultados
            return render(request, "Crud_Coche/coche_busqueda.html", contexto)

    # Si el formulario no es válido o no buscaron nada → mostrar formulario
    contexto = {"form": form}
    return render(request, "Crud_Coche/buscar_coches.html", contexto)

# -------------------------------------------------------------------
# Vista: Formulario para editar un coche existente
# -------------------------------------------------------------------
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
                messages.error(request, f"Error al guardar el coche: {e}")
    else:
        formulario = CocheModelForm(instance=coche)

    contexto = {'formulario': formulario, 'coche': coche}
    return render(request, 'Crud_Coche/editar_coche.html', contexto)

# -------------------------------------------------------------------
# VISTA: Eliminar un coche existente
# -------------------------------------------------------------------
def eliminar_coche(request, id_coche):
    coche = Coche.objects.get(id=id_coche)
    try:
        coche.delete()
        messages.success(request, "Coche eliminado correctamente.")
    except :
        pass
    return redirect('AlphaAutos:coche_list')

# -------------------------------------------------------------------
# Vista: Formulario para crear un nuevo concesionario
# -------------------------------------------------------------------
def crear_concesionario(request):
    if request.method == 'POST':
        form = ConcesionarioModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Concesionario creado correctamente.")
            return redirect('AlphaAutos:lista_concesionarios')
    else:
        form = ConcesionarioModelForm()
    
    contexto = {'form': form}
    return render(request, 'Crud_Concesionario/crear_concesionario.html', contexto)

# -------------------------------------------------------------------
# Vista: Formulario para buscar un concesionario 3 posibles filtros
# -------------------------------------------------------------------
def buscar_concesionarios(request):
    form = ConcesionarioSearchForm(request.GET or None)

    if len(request.GET) > 0:
        if form.is_valid():
            qs = Concesionario.objects.all()
            nombre = form.cleaned_data.get("nombre")
            ciudad = form.cleaned_data.get("ciudad")
            telefono = form.cleaned_data.get("telefono")

            if nombre:
                qs = qs.filter(nombre__icontains=nombre)
            if ciudad:
                qs = qs.filter(ciudad__icontains=ciudad)
            if telefono:
                qs = qs.filter(telefono__icontains=telefono)

            contexto = {"form": form, "concesionarios": qs}
            return render(request, "Crud_Concesionario/concesionario_busqueda.html", contexto)

    contexto = {"form": form}
    return render(request, "Crud_Concesionario/buscar_concesionarios.html", contexto)
# -------------------------------------------------------------------
# VISTA: Formulario para editar un concesionario existente
# -------------------------------------------------------------------
def editar_concesionario(request, id_concesionario):
    concesionario = get_object_or_404(Concesionario, id=id_concesionario)

    if request.method == 'POST':
        formulario = ConcesionarioModelForm(request.POST, instance=concesionario)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "Concesionario editado correctamente.")
                return redirect('AlphaAutos:concesionario_detail', id_concesionario=concesionario.id)
            except Exception as e:
                messages.error(request, f"Error al guardar el concesionario: {e}")
    else:
        formulario = ConcesionarioModelForm(instance=concesionario)

    contexto = {'formulario': formulario, 'concesionario': concesionario}
    return render(request, 'Crud_Concesionario/editar_concesionario.html', contexto)
# -------------------------------------------------------------------
# VISTA: Eliminar un concesionario existente
# -------------------------------------------------------------------
def eliminar_concesionario(request, id_concesionario):
    concesionario = Concesionario.objects.get(id=id_concesionario)
    try:
        concesionario.delete()
        messages.success(request, "Concesionario eliminado correctamente.")
    except :
        pass
    return redirect('AlphaAutos:lista_concesionarios')

# -------------------------------------------------------------------
# Vista: Formulario para crear una nueva marca 
# -------------------------------------------------------------------
def crear_marca(request):
    if request.method == 'POST':
        form = MarcaModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Marca creada correctamente.")
            return redirect('AlphaAutos:lista_marcas')
    else:
        form = MarcaModelForm()
    
    contexto = {'form': form}
    return render(request, 'Crud_Marca/crear_marca.html', contexto)

# -------------------------------------------------------------------
# Vista: Formulario para buscar una marca con 3 posibles filtros
# -------------------------------------------------------------------
def buscar_marcas(request):
    form = MarcaSearchForm(request.GET or None)

    if len(request.GET) > 0:
        if form.is_valid():
            qs = Marca.objects.all()
            nombre = form.cleaned_data.get("nombre")
            pais_origen = form.cleaned_data.get("pais_origen")
            anio_fundacion = form.cleaned_data.get("anio_fundacion")

            if nombre:
                qs = qs.filter(nombre__icontains=nombre)
            if pais_origen:
                qs = qs.filter(pais_origen__icontains=pais_origen)
            if anio_fundacion is not None:
                qs = qs.filter(anio_fundacion=anio_fundacion)

            contexto = {"form": form, "marcas": qs}
            return render(request, "Crud_Marca/marca_busqueda.html", contexto)

    contexto = {"form": form}
    return render(request, "Crud_Marca/buscar_marcas.html", contexto)

# -------------------------------------------------------------------
# VISTA: Mostrar una marca y sus coches relacionados
# -------------------------------------------------------------------
def marca_detail(request, id_marca):
    marca = get_object_or_404(Marca, id=id_marca)
    coches = marca.coche_set.select_related('concesionario').all()

    contexto = {
        'marca': marca,
        'coches': coches,
    }
    return render(request, 'concesionario/marca_detail.html', contexto)


# -------------------------------------------------------------------
# VISTA: Formulario para editar una marca existente
# -------------------------------------------------------------------
def editar_marca(request, id_marca):
    marca = get_object_or_404(Marca, id=id_marca)

    if request.method == 'POST':
        formulario = MarcaModelForm(request.POST, instance=marca)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "Marca editada correctamente.")
                return redirect('AlphaAutos:lista_marcas')
            except Exception as e:
                messages.error(request, f"Error al guardar la marca: {e}")
    else:
        formulario = MarcaModelForm(instance=marca)

    contexto = {'formulario': formulario, 'marca': marca}
    return render(request, 'Crud_Marca/editar_marca.html', contexto)

# ---------------------------------------------------
# Vista: Formulario para eliminar una marca existente
# ---------------------------------------------------
def eliminar_marca(request, id_marca):
    marca = Marca.objects.get(id=id_marca)
    try:
        marca.delete()
        messages.success(request, "Marca eliminada correctamente.")
    except :
        pass
    return redirect('AlphaAutos:lista_marcas')

# -------------------------------------------------------------------
# Vista: Formulario para crear un nuevo empleado
# -------------------------------------------------------------------
def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado creado correctamente.")
            return redirect('AlphaAutos:lista_empleados')
    else:
        form = EmpleadoModelForm()
    
    contexto = {'form': form}
    return render(request, 'Crud_Empleados/crear_empleados.html', contexto)

# -------------------------------------------------------------------
# Vista: Formulario para buscar un empleado con 3 posibles filtros
# -------------------------------------------------------------------
def buscar_empleados(request):
    form = EmpleadoSearchForm(request.GET or None)

    if len(request.GET) > 0:
        if form.is_valid():
            qs = Empleado.objects.all()
            nombre = form.cleaned_data.get("nombre")
            puesto = form.cleaned_data.get("puesto")
            concesionario = form.cleaned_data.get("concesionario")

            if nombre:
                qs = qs.filter(nombre__icontains=nombre)
            if puesto:
                qs = qs.filter(puesto__icontains=puesto)
            if concesionario:
                qs = qs.filter(concesionario=concesionario)

            contexto = {"form": form, "empleados": qs}
            return render(request, "Crud_Empleados/empleado_busqueda.html", contexto)

    contexto = {"form": form}
    return render(request, "Crud_Empleados/buscar_empleados.html", contexto)

# -------------------------------------------------------------------
# Vista: Formulario para eliminar empleado
# -------------------------------------------------------------------
def eliminar_empleado(request, id_empleado):
    empleado = Empleado.objects.get(id=id_empleado)
    try:
        empleado.delete()
        messages.success(request, "Empleado eliminado correctamente.")
    except :
        pass
    return redirect('AlphaAutos:lista_empleados')

# -------------------------------------------------------------------
# Vista: Formulario para crear un nuevo cliente
# -------------------------------------------------------------------
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente creado correctamente.")
            return redirect('AlphaAutos:lista_clientes')
    else:
        form = ClienteModelForm()
    
    contexto = {'form': form}
    return render(request, 'Crud_Clientes/crear_cliente.html', contexto)

# -------------------------------------------------------------------
# Vista: Formulario para buscar un cliente con 3 posibles filtros
# -------------------------------------------------------------------
def buscar_clientes(request):
    form = ClienteSearchForm(request.GET or None)

    if len(request.GET) > 0:
        if form.is_valid():
            qs = Cliente.objects.all()
            nombre = form.cleaned_data.get("nombre")
            email = form.cleaned_data.get("email")
            telefono = form.cleaned_data.get("telefono")

            if nombre:
                qs = qs.filter(nombre__icontains=nombre)
            if email:
                qs = qs.filter(email__icontains=email)
            if telefono:
                qs = qs.filter(telefono__icontains=telefono)

            contexto = {"form": form, "clientes": qs}
            return render(request, "Crud_Clientes/cliente_busqueda.html", contexto)

    contexto = {"form": form}
    return render(request, "Crud_Clientes/buscar_clientes.html", contexto)

# -------------------------------------------------------------------
# Vista: Formulario para crear una nueva aseguradora
# -------------------------------------------------------------------
def crear_aseguradora(request):
    if request.method == 'POST':
        form = AseguradoraModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Aseguradora creada correctamente.")
            return redirect('AlphaAutos:lista_aseguradoras')
    else:
        form = AseguradoraModelForm()
    
    contexto = {'form': form}
    return render(request, 'Crud_Aseguradora/crear_aseguradora.html', contexto)

# -------------------------------------------------------------------
# Vista: Formulario para buscar una aseguradora con 3 posibles filtros  
# -------------------------------------------------------------------
def buscar_aseguradoras(request):
    form = AseguradoraSearchForm(request.GET or None)

    if len(request.GET) > 0:
        if form.is_valid():
            qs = Aseguradora.objects.all()
            nombre = form.cleaned_data.get("nombre")
            pais = form.cleaned_data.get("pais")
            telefono = form.cleaned_data.get("telefono")

            if nombre:
                qs = qs.filter(nombre__icontains=nombre)
            if pais:
                qs = qs.filter(pais__icontains=pais)
            if telefono:
                qs = qs.filter(telefono__icontains=telefono)

            contexto = {"form": form, "aseguradoras": qs}
            return render(request, "Crud_Aseguradora/aseguradora_busqueda.html", contexto)

    contexto = {"form": form}
    return render(request, "Crud_Aseguradora/buscar_aseguradoras.html", contexto)


# -------------------------------------------------------------------
# VISTA: Mostrar detalle de empleado y editar
# -------------------------------------------------------------------
def empleado_detail(request, id_empleado):
    empleado = get_object_or_404(Empleado, id=id_empleado)
    contexto = {'empleado': empleado}
    return render(request, 'concesionario/empleado_detail.html', contexto)


def editar_empleado(request, id_empleado):
    empleado = get_object_or_404(Empleado, id=id_empleado)

    if request.method == 'POST':
        formulario = EmpleadoModelForm(request.POST, instance=empleado)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "Empleado editado correctamente.")
                return redirect('AlphaAutos:lista_empleados')
            except Exception as e:
                messages.error(request, f"Error al guardar el empleado: {e}")
    else:
        formulario = EmpleadoModelForm(instance=empleado)

    contexto = {'formulario': formulario, 'empleado': empleado}
    return render(request, 'Crud_Empleados/editar_empleados.html', contexto)


# -------------------------------------------------------------------
# VISTA: Mostrar detalle de cliente y editar
# -------------------------------------------------------------------
def cliente_detail(request, id_cliente):
    cliente = get_object_or_404(Cliente, id=id_cliente)
    contexto = {'cliente': cliente}
    return render(request, 'concesionario/cliente_detail.html', contexto)


def editar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id=id_cliente)

    if request.method == 'POST':
        formulario = ClienteModelForm(request.POST, instance=cliente)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "Cliente editado correctamente.")
                return redirect('AlphaAutos:lista_clientes')
            except Exception as e:
                messages.error(request, f"Error al guardar el cliente: {e}")
    else:
        formulario = ClienteModelForm(instance=cliente)

    contexto = {'formulario': formulario, 'cliente': cliente}
    return render(request, 'Crud_Clientes/editar_cliente.html', contexto)


# -------------------------------------------------------------------
# VISTA: Mostrar detalle de aseguradora y editar
# -------------------------------------------------------------------
def aseguradora_detail(request, id_aseguradora):
    aseguradora = get_object_or_404(Aseguradora, id=id_aseguradora)
    contexto = {'aseguradora': aseguradora}
    return render(request, 'concesionario/aseguradora_detail.html', contexto)


def editar_aseguradora(request, id_aseguradora):
    aseguradora = get_object_or_404(Aseguradora, id=id_aseguradora)

    if request.method == 'POST':
        formulario = AseguradoraModelForm(request.POST, instance=aseguradora)
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, "Aseguradora editada correctamente.")
                return redirect('AlphaAutos:lista_aseguradoras')
            except Exception as e:
                messages.error(request, f"Error al guardar la aseguradora: {e}")
    else:
        formulario = AseguradoraModelForm(instance=aseguradora)

    contexto = {'formulario': formulario, 'aseguradora': aseguradora}
    return render(request, 'Crud_Aseguradora/editar_aseguradora.html', contexto)

# -------------------------------------------------------------------
# VISTA: Eliminar un cliente existente
# -------------------------------------------------------------------
def eliminar_cliente(request, id_cliente):
    cliente = Cliente.objects.get(id=id_cliente)
    try:
        cliente.delete()
        messages.success(request, "Cliente eliminado correctamente.")
    except :
        pass
    return redirect('AlphaAutos:lista_clientes')

# -------------------------------------------------------------------
# VISTA: Eliminar una aseguradora existente
# -------------------------------------------------------------------
def eliminar_aseguradora(request, id_aseguradora):
    aseguradora = Aseguradora.objects.get(id=id_aseguradora)
    try:
        aseguradora.delete()
        messages.success(request, "Aseguradora eliminada correctamente.")
    except :
        pass
    return redirect('AlphaAutos:lista_aseguradoras')