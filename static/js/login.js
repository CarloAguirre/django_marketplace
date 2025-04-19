document.addEventListener("DOMContentLoaded",()=>{
    const loginButton = document.querySelector(".btn-info.text-white.w-100"); 
    const usernameInput = document.querySelector(".input-group.mt-4 input"); 
    const passwordInput = document.querySelector(".input-group.mt-1 input"); 
    const rememberMeCheckbox = document.querySelector(".form-check-input");

    if (!loginButton || !usernameInput || !passwordInput) {
        console.error("No se encontraron los elementos del formulario de login.");
        return;
    }

    loginButton.addEventListener("click", () => {
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();
        const rememberMe = rememberMeCheckbox.checked;

        if (username === "" || password === "") {
            alert("Por favor, complete todos los campos.")
            return
        }

        let users = JSON.parse(localStorage.getItem("usuarios")) || []

        let userFound = users.find(user => user.username === username && user.password === password)

        if (userFound) {
            if (rememberMe) {
                localStorage.setItem("usuarioActivo", JSON.stringify(userFound))
            } else {
                sessionStorage.setItem("usuarioActivo", JSON.stringify(userFound))
            }

            alert("Inicio de sesión exitoso!")
            window.location.href = "index.html"
        } else {
            alert("Usuario o contraseña incorrectos.")
        }
    })
})
