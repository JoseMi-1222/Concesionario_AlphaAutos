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
    return render(request, "concesionario/index.html")

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
# VISTA: Listar coches fabricados en un año y mes concretos
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
# Vista: Formulario para crear un nuevo coche
# -------------------------------------------------------------------
def crear_coche(request):
    if request.method == 'POST':
        form = CocheModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Coche creado correctamente.")
            return redirect('AlphaAutos:coche_list')
    else:
        form = CocheModelForm()
    
    contexto = {'form': form}
    return render(request, 'Crud_Coche/crear_coche.html', contexto)

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