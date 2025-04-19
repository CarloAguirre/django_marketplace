from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from .models import Direccion, Rol, Carrito, CarritoProducto, Producto
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import Producto, Categoria
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.http import require_POST
import json


User = get_user_model()


# Create your views here.

def index(request):
	return render(request, 'core/index.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('perfil')

    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('perfil')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, 'core/login.html')


User = get_user_model()

def registro(request):
    if request.method == 'POST':
        nombres       = request.POST.get('nombres', '').strip()
        apellidos     = request.POST.get('apellidos', '').strip()
        username      = request.POST.get('username', '').strip()
        email         = request.POST.get('email', '').strip()
        password      = request.POST.get('password', '')
        repassword    = request.POST.get('repassword', '')
        fecha_nac     = request.POST.get('fecha_nacimiento') 
        calle         = request.POST.get('calle', '').strip()
        numero_calle  = request.POST.get('numero', '').strip()
        tipo_dir      = request.POST.get('tipo_direccion', '').strip()
        if password != repassword:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'core/registro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return render(request, 'core/registro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo ya está registrado.")
            return render(request, 'core/registro.html')
        direccion = None
        if calle or numero_calle or tipo_dir:
            try:
                num = int(numero_calle) if numero_calle else 0
            except ValueError:
                messages.error(request, "Ingrese un número de calle válido.")
                return render(request, 'core/registro.html')

            direccion = Direccion.objects.create(
                calle=calle or "-",
                numero=num,
                depto=tipo_dir or None
            )
        rol_usuario, _ = Rol.objects.get_or_create(nombre_rol='usuario')
        usuario = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            nombre=nombres,
            apellido=apellidos,
            fecha_nacimiento=fecha_nac or None,
            direccion=direccion,
            rol=rol_usuario
        )
        login(request, usuario)
        messages.success(request, f"Bienvenido, {usuario.nombre}! Tu cuenta ha sido creada.")
        return redirect('perfil')
    return render(request, 'core/registro.html')


def productos(request):
    lista_productos = Producto.objects.all()
    return render(request, 'core/productos.html', {
        'productos': lista_productos
    })

def categorias(request):
    todas = Categoria.objects.all()
    return render(request, 'core/categorias.html', {'categorias': todas})

# core/views.py
def categoria(request, id, slug):
    categoria = get_object_or_404(Categoria, id=id)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'core/categoria.html',{
        'categoria': categoria,
        'productos': productos
    })


@login_required
def perfil(request):
    productos = Producto.objects.all()
    return render(request, 'core/perfil.html', {
        'productos': productos
    })

@login_required
def nuevo_producto(request):
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        nombre       = request.POST.get('nombre', '').strip()
        categoria_id = request.POST.get('categoria')
        imagen_file  = request.FILES.get('imagen')
        descripcion  = request.POST.get('descripcion', '').strip()
        stock        = request.POST.get('stock', '0')
        precio       = request.POST.get('precio', '0')

        if not nombre or not categoria_id or not imagen_file:
            messages.error(request, "Complete todos los campos obligatorios.")
            return render(request, 'core/nuevo_producto.html', {'categorias': categorias})

        try:
            categoria = Categoria.objects.get(pk=categoria_id)
        except Categoria.DoesNotExist:
            messages.error(request, "Categoría no válida.")
            return render(request, 'core/nuevo_producto.html', {'categorias': categorias})
        fs = FileSystemStorage()
        relative_path = fs.save(f'productos/{imagen_file.name}', imagen_file)
        producto = Producto.objects.create(
            nombre      = nombre,
            descripcion = descripcion,
            stock       = int(stock),
            precio      = precio,
            categoria   = categoria,
            imagen      = relative_path
        )

        messages.success(request, f"Producto “{producto.nombre}” creado correctamente.")
        return redirect('perfil')

    return render(request, 'core/nuevo_producto.html', {
        'categorias': categorias
    })


def producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'core/producto.html', {'producto': producto})


@csrf_exempt
def actualizar_producto(request, id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=id)
        data = json.loads(request.body)
        producto.nombre = data.get('nombre', producto.nombre)
        producto.stock = data.get('stock', producto.stock)
        producto.precio = data.get('precio', producto.precio)
        producto.save()
        return JsonResponse({'status': 'ok'})


@require_POST
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('perfil')

@csrf_exempt
@require_POST
@login_required
def agregar_al_carrito(request):
    try:
        producto_id = request.POST.get("producto_id")
        cantidad = int(request.POST.get("cantidad", 1))

        producto = get_object_or_404(Producto, id=producto_id)
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user, estado='A')

        item, creado = CarritoProducto.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': cantidad}
        )

        if not creado:
            item.cantidad += cantidad
            item.save()

        total_items = CarritoProducto.objects.filter(carrito=carrito).count()
        return JsonResponse({"ok": True, "total_items": total_items})
    
    except Exception as e:
        print("⚠️ Error en agregar_al_carrito:", e)
        return JsonResponse({"ok": False, "error": str(e)}, status=500)


@login_required
def obtener_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user, estado='A').first()
    productos = []

    if carrito:
        for item in carrito.carritoproducto_set.select_related('producto'):
            productos.append({
                "id": item.producto.id,
                "nombre": item.producto.nombre,
                "precio": float(item.producto.precio),
                "cantidad": item.cantidad,
                "imagen": item.producto.imagen.url if item.producto.imagen else ""
            })

    return JsonResponse({"productos": productos})


def listar_carrito(request):
    if not request.user.is_authenticated:
        return JsonResponse({'items': [], 'total_items': 0})

    carrito = Carrito.objects.filter(usuario=request.user, estado='A').first()
    if not carrito:
        return JsonResponse({'items': [], 'total_items': 0})

    items = []
    total_items = 0

    for item in CarritoProducto.objects.filter(carrito=carrito):
        items.append({
            'id':       item.producto.id,
            'nombre':   item.producto.nombre,
            'precio':   float(item.producto.precio),
            'cantidad': item.cantidad,
            'imagen':   item.producto.imagen.url if item.producto.imagen else ""
        })
        total_items += item.cantidad

    return JsonResponse({'items': items, 'total_items': total_items})



@require_POST
@login_required
def modificar_cantidad_carrito(request):
    producto_id = request.POST.get("producto_id")
    cantidad = int(request.POST.get("cantidad"))

    producto = get_object_or_404(Producto, id=producto_id)
    carrito = get_object_or_404(Carrito, usuario=request.user, estado="A")
    item = get_object_or_404(CarritoProducto, carrito=carrito, producto=producto)

    item.cantidad = cantidad
    item.save()

    return JsonResponse({"ok": True})


@require_POST
@login_required
def eliminar_producto_carrito(request):
    producto_id = request.POST.get("producto_id")
    carrito = get_object_or_404(Carrito, usuario=request.user, estado="A")
    CarritoProducto.objects.filter(carrito=carrito, producto_id=producto_id).delete()
    total_items = CarritoProducto.objects.filter(carrito=carrito).count()
    return JsonResponse({"ok": True, "total_items": total_items})