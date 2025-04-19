document.addEventListener("DOMContentLoaded", ()=>{
    const params = new URLSearchParams(window.location.search);
    const productoIndex = params.get("id")

    if (productoIndex === null) {
        document.body.innerHTML = "<h1>Producto no encontrado</h1>";
        return
    }

    const productos = JSON.parse(localStorage.getItem("productos")) || [];
    if (!productos[productoIndex]) {
        document.body.innerHTML = "<h1>Producto no encontrado</h1>"
        return
    }

    const producto = productos[productoIndex]
    document.getElementById("producto-nombre").textContent = producto.nombre
    document.getElementById("producto-nombre-header").textContent = producto.nombre
    
    const imagenElemento = document.getElementById("producto-imagen")
    if (imagenElemento) {
        imagenElemento.src = producto.imagen ? producto.imagen : 'Imagen no disponible'
    }
    document.getElementById("producto-descripcion").textContent = producto.descripcion

    const precioElemento = document.getElementById("producto-precio")
    if (precioElemento) {
        precioElemento.textContent = producto.precio ? `$${producto.precio}` : "No disponible"
        precioElemento.style.fontWeight = "bold"; 
    }
    const listaIzquierda = document.getElementById("caracteristicas-izquierda")
    const listaDerecha = document.getElementById("caracteristicas-derecha")
    if (listaIzquierda && listaDerecha) {
        listaIzquierda.innerHTML = ""
        listaDerecha.innerHTML = ""

        producto.caracteristicas.forEach((caracteristica, index) => {
            let li = document.createElement("li")
            li.textContent = caracteristica
            if (index % 2 === 0) {
                listaIzquierda.appendChild(li)
            } else {
                listaDerecha.appendChild(li)
            }
        });
    }
});
