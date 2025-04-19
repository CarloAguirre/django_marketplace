
document.addEventListener("DOMContentLoaded", () => {
    const nav = document.querySelector(".navbar-nav")

    if (!nav) {
        console.error("No se encontró el menú de navegación.")
        return
    }

    const usuarioActivo = JSON.parse(localStorage.getItem("usuarioActivo")) || JSON.parse(sessionStorage.getItem("usuarioActivo"))

    if (usuarioActivo) {
        ocultarLinks(["registro.html", "login.html"])
        mostrarLinks(["perfil/perfil.html"]) 

        const logoutItem = document.createElement("li")
        logoutItem.classList.add("nav-item")
        logoutItem.innerHTML = `<a class="nav-link text-danger" href="#" id="logout-btn">Cerrar Sesión</a>`
        nav.appendChild(logoutItem)

        document.getElementById("logout-btn").addEventListener("click", () => {
            localStorage.clear()
            sessionStorage.clear()
            alert("Has cerrado sesión y se han eliminado todos los datos almacenados.")
            location.reload()
        })        
        
    } else {
        mostrarLinks(["registro.html", "login.html"])
        ocultarLinks(["perfil/perfil.html"])
    }
})

function ocultarLinks(urls) {
    document.querySelectorAll(".nav-item a").forEach(link => {
        let linkHref = link.getAttribute("href").replace(/^(\.\/)+/, '') 
        let match = urls.some(url => linkHref.endsWith(url.replace(/^(\.\/)+/, '')))

        if (match) {
            link.parentElement.style.display = "none"
        }
    })
}

function mostrarLinks(urls) {
    document.querySelectorAll(".nav-item a").forEach(link => {
        let linkHref = link.getAttribute("href").replace(/^(\.\/)+/, '') 
        let match = urls.some(url => linkHref.endsWith(url.replace(/^(\.\/)+/, '')))

        if (match) {
            link.parentElement.style.display = "block"
        }
    })
}


const inputs = {
	nombres : document.getElementById('input-nombres'),
	apellidos : document.getElementById('input-apellidos'),
	username : document.getElementById('input-usuario'),
	email : document.getElementById('input-email'),
	password : document.getElementById('input-pass'),
	repeatPassword : document.getElementById('input-repass'),
	nacimiento : document.getElementById('input-birthday'),
	calle : document.getElementById('input-calle'),
	numeroCalle : document.getElementById('input-numero'),
	tipoDireccion : document.getElementById('input-tipo_direccion')
};

let errors = 0;

document.getElementById('form-user').addEventListener("submit", (event) => {
    event.preventDefault();
    let errors = 0;

    for (let input in inputs) {
        const divPadre = inputs[input].parentElement;
        let errorExistente = divPadre.querySelector('.error-msg');
        if (errorExistente) {
            divPadre.removeChild(errorExistente);
        }
    }

    for (let input in inputs) {
        if (input !== "tipoDireccion" && inputs[input].value.trim().length <= 1) {
            mostrarError(inputs[input], `Introduzca un valor válido`);
            return;
        }
        if (input === "email" && inputs[input].value.length >= 1) {
            const esMail = inputs[input].value.split('@');
            if (esMail.length < 2) {
                mostrarError(inputs[input], "El formato del correo es incorrecto");
                return;
            }
        }
    }

    if (inputs.password.value !== inputs.repeatPassword.value) {
        alert('Las contraseñas deben coincidir');
        return;
    }
    if (inputs.password.value.length < 6 || inputs.password.value.length > 18) {
        alert('La contraseña debe tener entre 6 y 18 caracteres');
        return;
    }
    if (!inputs.password.value.split('').some(char => !isNaN(char))) {
        alert('La contraseña debe tener al menos un número');
        return;
    }
    if (!inputs.password.value.split('').some(char => char !== char.toLowerCase())) {
        alert('La contraseña debe tener al menos una mayúscula');
        return;
    }

    const fechaIngresada = new Date(inputs.nacimiento.value);
    let fechaActual = new Date();
    let edad = fechaActual.getFullYear() - fechaIngresada.getFullYear();
    const mesActual = fechaActual.getMonth();
    const diaActual = fechaActual.getDate();
    const mesNac = fechaIngresada.getMonth();
    const diaNac = fechaIngresada.getDate();

    if (mesActual < mesNac || (mesActual === mesNac && diaActual < diaNac)) {
        edad--;
    }

    if (edad < 13) {
        alert('Debes tener al menos 13 años para registrarte');
        return;
    }

    if (errors == 0) {
        let usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];

        let nuevoUsuario = {
            username: inputs.username.value.trim(),
            email: inputs.email.value.trim(),
            password: inputs.password.value.trim(),
            nombre: inputs.nombres.value.trim(),
            apellidos: inputs.apellidos.value.trim()
        };

        usuarios.push(nuevoUsuario);
        localStorage.setItem("usuarios", JSON.stringify(usuarios));

        alert('Usuario registrado con éxito!');
        window.location.href = 'login.html'; 
    }
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
document.getElementById('boton-cancelar').addEventListener('click', () =>{
	for (let input in inputs){
		const divPadre = inputs[input].parentElement
		let errorExistente = divPadre.querySelector('.error-msg')
		if (errorExistente){
			divPadre.removeChild(errorExistente)
		}
	}
	errors = 0
})
let iconCart = document.querySelector('.icon-cart')
let closeCart = document.querySelector('.cerrar')
let body = document.querySelector('body')
iconCart.addEventListener('click', () => {
	body.classList.toggle('showCart');
})
closeCart.addEventListener('click', () => {
	body.classList.toggle('active');
})


