Este proyecto utiliza Django conectado a Oracle Cloud usando el cliente cx_Oracle y un wallet integrado. La estructura ya incluye formularios de registro e inicio de generados con Django authentication system, ademas de "roles" como "IS_SUPERUSER", "IS_STAFF" (https://docs.djangoproject.com/en/5.1/topics/auth/default/)

🚧 Requisitos
- Python 3.10.6 o versiones anteriores (muy recomendable, versiones distintas pueden causar errores con cx_Oracle)

- Git

- Acceso a Oracle Cloud + archivos del wallet (ya incluidos en core/db/wallet)

- Oracle Instant Client instalado y agregado al PATH

🚀 Configurar el proyecto

2. Crear entorno virtual
 ```python -m venv venv310```
 
3. Activar entorno virtual
En CMD de Windows:
```venv310\Scripts\activate```

En Git Bash:
```source venv310/Scripts/activate```

4. Instalar dependencias
```pip install -r requirements.txt```

4. Configurar la ruta de la wallet en el archivo 'core/db/wallet/sqlnet.ora'. Debe reflejar la ruta real en la que este la carpeta wallet en su computador, por ejemplo: 'DIRECTORY=C:\Users\usuario\Desktop\primer_django_app\core\db\wallet'