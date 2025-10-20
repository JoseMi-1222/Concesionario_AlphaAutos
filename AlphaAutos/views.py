from django.shortcuts import render

# -------------------------------
# VISTA: Página inicial (Index)
# -------------------------------
def index(request):
    """
    Vista inicial que muestra enlaces a las diferentes URLs de la aplicación.

    SQL equivalente:
    -- No aplica: sólo renderiza la plantilla index.html
    """
    return render(request, "concesionario/index.html")
