// Espera a que el DOM cargue
document.addEventListener('DOMContentLoaded', () => {
    console.log("AlphaAutos cargado correctamente");

    // Ejemplo: Resaltar el menú actual
    const links = document.querySelectorAll('nav ul li a');
    links.forEach(link => {
        if (link.href === window.location.href) {
            link.style.textDecoration = "underline";
        }
    });
});

function eliminar(){
    var x = confirm("¿Estás seguro de que deseas eliminar?");
    if (x)
        return true;
    else
        return false;
}