document.addEventListener("DOMContentLoaded",()=> {
	const contenedorProductos = document.querySelector(".user-products-container")
	const productos = JSON.parse(localStorage.getItem("productos")) || []
	if (productos.length === 0){
	  return;
	}
  
	productos.forEach((producto, index)=> {
	  const productoHTML = `
		<div class="box">
		  <div class="cont-img">
			<img src="${producto.imagen}" class="cont-img" alt="Imagen del producto">
			<div class="img-overlay">
			  <div class="img-title">
				<a href="../../productos/producto.html?id=${index}" class="nav-link">${producto.nombre}</a>
			  </div>
			  <p class="img-description">${producto.descripcion}</p>
			  <p class="img-description"><strong>Precio:</strong> $${producto.precio}</p>
			</div>
		  </div>
		</div>
	  `
	  contenedorProductos.innerHTML += productoHTML
	})
  })
  
  document.addEventListener("DOMContentLoaded", () => {
    const usuarioActivo = JSON.parse(localStorage.getItem("usuarioActivo")) || JSON.parse(sessionStorage.getItem("usuarioActivo"))

    const nombreElemento = document.querySelector(".user-info:nth-of-type(1) p")
    const emailElemento = document.querySelector(".user-info:nth-of-type(2) p")

    if (usuarioActivo) {
        nombreElemento.textContent = usuarioActivo.nombre || "Usuario Desconocido"
        emailElemento.textContent = usuarioActivo.email || "Email no registrado"
    } else {
        alert("No has iniciado sesión. Serás redirigido al inicio.")
        window.location.href = "../index.html"
    }
})
