from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.ForeignKey('Direccion', on_delete=models.SET_NULL, null=True)
    rol = models.ForeignKey('Rol', on_delete=models.SET_NULL, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        related_name='usuario_set',
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuario_set',
        blank=True,
        help_text='Permisos específicos para este usuario.'
    )

    REQUIRED_FIELDS = ['email', 'nombre', 'apellido']

    def __str__(self):
        return self.username



class Rol(models.Model):
    nombre_rol = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre_rol

class Direccion(models.Model):
    calle = models.CharField(max_length=60)
    numero = models.IntegerField()
    depto = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.calle} {self.numero}"


class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=30)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre_categoria

class Producto(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(
                                    settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='mis_productos',
                                    null=True,  
                                    blank=True
                                    )

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=1, choices=[('A', 'Abierto'), ('C', 'Cerrado')], default='A')

    def __str__(self):
        return f"Carrito #{self.id} - {self.usuario.username}"

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} en carrito {self.carrito.id}"

class Compra(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    fecha_compra = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20)

    def __str__(self):
        return f"Compra #{self.id} - {self.usuario.username}"
