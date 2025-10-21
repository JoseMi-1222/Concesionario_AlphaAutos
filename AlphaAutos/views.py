from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from django.utils import timezone


# -------------------------------
# VISTA: Página inicial (Index)
# -------------------------------
def index(request):
    """
    Vista inicial que muestra enlaces a las diferentes URLs de la aplicación.

    SQL:
    -- No aplica: sólo renderiza la plantilla index.html
    """
    return render(request, "concesionario/index.html")

# --------------------------------------------------
# VISTA: Listar todos los coches con sus relaciones
# --------------------------------------------------
def coche_list(request):
    """
    Muestra todos los coches con su marca y concesionario.
    Usa select_related para optimizar las consultas.

    SQL:
    SELECT c.id, c.modelo, c.precio, m.nombre AS marca, con.nombre AS concesionario
    FROM AlphaAutos_coche c
    INNER JOIN AlphaAutos_marca m ON c.marca_id = m.id
    INNER JOIN AlphaAutos_concesionario con ON c.concesionario_id = con.id
    ORDER BY m.nombre;
    """
    coches = Coche.objects.select_related('marca', 'concesionario').order_by('marca__nombre')
    contexto = {'coches': coches}
    return render(request, 'concesionario/coche_list.html', contexto)

# ------------------------------------------------------------
# VISTA: Mostrar un coche concreto mediante su id (int)
# ------------------------------------------------------------
def coche_detail(request, id_coche):
    """
    Muestra todos los datos de un coche concreto, incluyendo su marca
    y su concesionario. Usa get_object_or_404 para asegurar la existencia.

    SQL equivalente aproximada:
    SELECT c.id, c.modelo, c.precio, c.transmision, c.fecha_fabricacion,
           m.nombre AS marca, con.nombre AS concesionario
    FROM AlphaAutos_coche c
    INNER JOIN AlphaAutos_marca m ON c.marca_id = m.id
    INNER JOIN AlphaAutos_concesionario con ON c.concesionario_id = con.id
    WHERE c.id = id_coche;
    """
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
    """
    Muestra los coches cuya fecha de fabricación coincide con el año y mes indicados.

    SQL equivalente aproximada:
    SELECT * FROM AlphaAutos_coche
    WHERE EXTRACT(YEAR FROM fecha_fabricacion) = anio
      AND EXTRACT(MONTH FROM fecha_fabricacion) = mes
    ORDER BY fecha_fabricacion DESC;
    """
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
    """
    Muestra los coches con transmisión del tipo indicado o manual.
    Se usa Q() para aplicar un filtro con OR.

    SQL equivalente aproximada:
    SELECT * FROM AlphaAutos_coche
    WHERE transmision = tipo OR transmision = 'MT'
    ORDER BY marca_id;
    """
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
    """
    Muestra los coches de un concesionario cuyo modelo contenga el texto indicado.
    Se usa un filtro con AND (concesionario y texto en modelo).

    SQL equivalente aproximada:
    SELECT c.id, c.modelo, c.precio, m.nombre AS marca, con.nombre AS concesionario
    FROM AlphaAutos_coche c
    INNER JOIN AlphaAutos_marca m ON c.marca_id = m.id
    INNER JOIN AlphaAutos_concesionario con ON c.concesionario_id = con.id
    WHERE con.id = id_concesionario AND c.modelo LIKE '%texto%';
    """
    coches = Coche.objects.filter(
        concesionario_id=id_concesionario,
        modelo__icontains=texto  # AND implícito
    ).select_related('marca', 'concesionario').order_by('marca__nombre')

    concesionario = Concesionario.objects.get(id=id_concesionario)

    contexto = {
        'coches': coches,
        'texto': texto,
        'concesionario': concesionario,
    }
    return render(request, 'concesionario/coches_concesionario_texto.html', contexto)

# -------------------------------------------------------------------
# VISTA: Coches de un concesionario cuyo modelo contiene un texto
# -------------------------------------------------------------------
def coches_concesionario_texto(request, id_concesionario, texto):
    """
    Muestra los coches de un concesionario cuyo modelo contenga el texto indicado.
    Se usa un filtro con AND (concesionario y texto en modelo).

    SQL equivalente aproximada:
    SELECT c.id, c.modelo, c.precio, m.nombre AS marca, con.nombre AS concesionario
    FROM AlphaAutos_coche c
    INNER JOIN AlphaAutos_marca m ON c.marca_id = m.id
    INNER JOIN AlphaAutos_concesionario con ON c.concesionario_id = con.id
    WHERE con.id = id_concesionario AND c.modelo LIKE '%texto%';
    """
    coches = Coche.objects.filter(
        concesionario_id=id_concesionario,
        modelo__icontains=texto  # AND implícito
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
    """
    Obtiene el último cliente que compró el coche indicado.
    Se accede a través de la tabla intermedia 'Venta' (N:M).

    SQL equivalente aproximada:
    SELECT cliente_id
    FROM AlphaAutos_venta
    WHERE coche_id = id_coche
    ORDER BY fecha_venta DESC
    LIMIT 1;
    """
    # Usamos select_related para optimizar (accede a cliente y coche)
    ultima_venta = Venta.objects.select_related('cliente', 'coche').filter(
        coche_id=id_coche
    ).order_by('-fecha_venta').first()  # LIMIT 1

    contexto = {
        'venta': ultima_venta
    }
    return render(request, 'concesionario/ultimo_cliente_coche.html', contexto)

# --------------------------------------------------------------------
# VISTA: Mostrar coches que no tienen ventas (isnull=True)
# --------------------------------------------------------------------
def coches_sin_ventas(request):
    """
    Muestra los coches que no tienen ventas asociadas (sin relación en la tabla intermedia 'Venta').
    Se usa un filtro con isnull=True sobre la relación reversa 'venta'.

    SQL equivalente aproximada:
    SELECT c.id, c.modelo, c.precio
    FROM AlphaAutos_coche c
    LEFT JOIN AlphaAutos_venta v ON c.id = v.coche_id
    WHERE v.id IS NULL;
    """
    coches = Coche.objects.filter(venta__isnull=True).select_related('marca', 'concesionario').order_by('marca__nombre')

    contexto = {'coches': coches}
    return render(request, 'concesionario/coches_sin_ventas.html', contexto)

# -------------------------------------------------------------------
# VISTA: Mostrar un concesionario y sus relaciones (empleados, coches)
# -------------------------------------------------------------------
def concesionario_detail(request, id_concesionario):
    """
    Muestra los datos de un concesionario junto con sus empleados y coches.
    Usa relaciones reversas (empleado_set y coche_set) y prefetch_related.

    SQL equivalente aproximada:
    SELECT * FROM AlphaAutos_concesionario WHERE id = id_concesionario;
    SELECT * FROM AlphaAutos_empleado WHERE concesionario_id = id_concesionario;
    SELECT * FROM AlphaAutos_coche WHERE concesionario_id = id_concesionario;
    """
    concesionario = Concesionario.objects.prefetch_related('empleado_set', 'coche_set').get(id=id_concesionario)
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
        precio_promedio=Avg('precio_final'),
        precio_maximo=Max('precio_final'),
        precio_minimo=Min('precio_final')
    )

    contexto = {
        'resumen': resumen
    }
    return render(request, 'concesionario/resumen_ventas.html', contexto)