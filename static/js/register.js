document.addEventListener("DOMContentLoaded", ()=>{
	const inputs = {
	  nombre: document.getElementById('input-nombres'),
	  descripcion: document.getElementById('descripcion'),
	  c1: document.getElementById('c1'),
	  c2: document.getElementById('c2'),
	  c3: document.getElementById('c3'),
	  c4: document.getElementById('c4'),
	  c5: document.getElementById('c5'),
	  c6: document.getElementById('c6'),
	  precio: document.getElementById('input-precio'),
	  imagen: document.getElementById('input-imagen')
	};
  
	let errors = 0
  
	document.getElementById('form-user').addEventListener("submit", (event)=>{
	  event.preventDefault()
	  errors = 0
	  for (let input in inputs){
		const divPadre = inputs[input].parentElement
		let errorExistente = divPadre.querySelector('.error-msg')
		if (errorExistente){
		  divPadre.removeChild(errorExistente)
		}
	  }
	  for (let input in inputs) {
		const valor = inputs[input].value.trim();
		if (input !== "imagen" && valor.length === 0){
		  mostrarError(inputs[input], `El campo ${input} no puede estar vacío`)
		}
	  }
	  if (!/^\d+(\.\d{1,2})?$/.test(inputs.precio.value)){
		mostrarError(inputs.precio, "Ingrese un precio válido (números y opcionalmente hasta dos decimales).")
	  }
	  if (!inputs.imagen.files.length){
		mostrarError(inputs.imagen, "Debe seleccionar una imagen.")
	  }
  
	  if (errors > 0) return
  
	  // profesor, aca se esta procesando la imagen en Base64
	  const file = inputs.imagen.files[0]
	  const reader = new FileReader()
  
	  reader.readAsDataURL(file)
	  reader.onload = function(){
	  const imagenBase64 = reader.result
  
	const producto ={
		nombre: inputs.nombre.value,
		descripcion: inputs.descripcion.value,
		caracteristicas: [
		inputs.c1.value, inputs.c2.value, inputs.c3.value,
		inputs.c4.value, inputs.c5.value, inputs.c6.value
		].filter(c => c.trim() !== ""),
		precio: inputs.precio.value,
		imagen: imagenBase64
	};
		let productos = JSON.parse(localStorage.getItem("productos")) || []
		productos.push(producto)
		localStorage.setItem("productos", JSON.stringify(productos))
  
		document.getElementById('form-user').reset()
  
		alert("Producto guardado correctamente.")
		window.location.href = './perfil.html';
	  };
  
	  reader.onerror = function(){
		alert("Error al leer la imagen.")
	  };
	});
	function mostrarError(input, mensaje){
	  const divPadre = input.parentElement
	  let errorMsg = document.createElement('p')
	  errorMsg.classList.add('error-msg')
	  errorMsg.style.color = "red"
	  errorMsg.style.fontSize = "14px"
	  errorMsg.style.marginTop = "5px"
	  errorMsg.textContent = mensaje
	  divPadre.appendChild(errorMsg)
	  errors += 1
	}

	document.getElementById('boton-cancelar').addEventListener('click', () => {
	  for (let input in inputs) {
		const divPadre = inputs[input].parentElement
		let errorExistente = divPadre.querySelector('.error-msg')
		if (errorExistente) {
		  divPadre.removeChild(errorExistente)
		}
	  }
	  errors = 0
	})
  })
  