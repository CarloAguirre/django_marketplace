document.addEventListener("DOMContentLoaded", () => {
	const productContent = document.querySelector('.product-content')
	const productosLS = JSON.parse(localStorage.getItem("productos")) || []
	if (productContent && productosLS.length > 0) {
	  productosLS.forEach((producto, index) => {
		const productBox = document.createElement("div")
		productBox.classList.add("product-box")
		productBox.innerHTML = `
		  <div class="img-box">
			<img src="${producto.imagen}" alt="Imagen de ${producto.nombre}"/>
		  </div>
		  <a href="./producto.html?id=${index}">
			<h2 class="name">${producto.nombre}</h2>
		  </a>
		  <p class="img-description">${producto.descripcion}</p>
		  <div class="price-and-cart">
			<span class="price">$${producto.precio}</span>
			<button class="addCart">Añadir al carrito</button>
		  </div>
		`
		productContent.appendChild(productBox)
	  })
	}
  })
  