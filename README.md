🚀 Configurar el proyecto

1. Crear entorno virtual
 ```python -m venv venv```
 
2. Activar entorno virtual
En CMD de Windows:
```venv\Scripts\activate```

En Git Bash:
```source venv/Scripts/activate```

3. Instalar dependencias
```pip install -r requirements.txt```

📌 Al momento de registrarse se debe seleccionar el rol del usuario creado. Tanto el "Admin" como el "Usuario" tienen funcionalidades diferente definidas en la interfaz de "perfil"

- Documentación completa de la API creada
https://documenter.getpostman.com/view/22825210/2sB2j4eAVX#8f046ace-c467-496d-b865-ab3c39306c54

🌐 APIs Externas Consumidas
- GiantBomb API
Se consulta dinámicamente una selección aleatoria de videojuegos clásicos para mostrar en el slider de la página principal (index.html).
Cada vez que el usuario carga la página, se obtienen 4 juegos aleatorios con:

- UUIDGenerator API
Se utiliza para simular un sistema de generación de códigos promocionales.
Al entrar a la página principal, después de 3 segundos se muestra un modal con un código aleatorio generado desde esta API, cumpliendo con el requisito de mostrar datos externos de manera contextual al usuario.