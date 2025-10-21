from django.shortcuts import render
from .models import Coche
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


