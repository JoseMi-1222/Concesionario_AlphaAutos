from django.shortcuts import render

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

from .models import Coche

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

from django.shortcuts import get_object_or_404
from .models import Coche

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

