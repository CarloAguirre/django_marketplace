import cx_Oracle

conn = cx_Oracle.connect(
    user="django_user",
    password="OracleLocal123", 
    dsn="localhost/XEPDB1" 
)

print("¡Conectado correctamente a Oracle Local!")
