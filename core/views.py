from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from .models import Direccion, Rol, Carrito, CarritoProducto, Producto, Compra
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import Producto, Categoria
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.http import require_POST
from django.db.models import F
import re
import json
import requests, random




User = get_user_model()


def index(request):
    api_key = '7ce8a89a5d9431cdb3c95f91830c39b67d6170b8'
    headers = {'User-Agent': 'TuApp/1.0'}

    meta_resp = requests.get(
        'https://www.giantbomb.com/api/games/',
        params={'api_key': api_key, 'format': 'json', 'limit': 1},
        headers=headers
    )
    meta = meta_resp.json()
    total = meta.get('number_of_total_results', 0)
    offset = random.randint(0, max(total - 4, 0))

    response = requests.get(
        'https://www.giantbomb.com/api/games/',
        params={'api_key': api_key, 'format': 'json', 'limit': 3, 'offset': offset},
        headers=headers
    ).json()
    juegos = response.get('results', [])

    destacados = []
    for juego in juegos:
        if juego.get('image') and juego.get('deck') and juego.get('site_detail_url'):
            destacados.append({
                'name': juego['name'],
                'deck': juego['deck'],
                'image': juego['image']['original_url'],
                'url': juego['site_detail_url']
            })

    return render(request, 'core/index.html', {
        'categorias': Categoria.objects.all(),
        'destacados': destacados
    })



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


def registro(request):
    if request.method == 'POST':
        nombres = request.POST.get('nombres', '').strip()
        apellidos = request.POST.get('apellidos', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        repassword = request.POST.get('repassword', '')
        fecha_nac = request.POST.get('fecha_nacimiento')
        calle = request.POST.get('calle', '').strip()
        numero_calle = request.POST.get('numero', '').strip()
        tipo_dir = request.POST.get('tipo_direccion', '').strip()

        if password != repassword:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'core/registro.html')

        if len(password) < 8 or len(password) > 64:
            messages.error(request, "La contraseña debe tener entre 8 y 64 caracteres.")
            return render(request, 'core/registro.html')

        import re
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            messages.error(request, "La contraseña debe contener al menos una letra y un número.")
            return render(request, 'core/registro.html')
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\'\"\\|,.<>\/?]', password):
            messages.error(request, "La contraseña debe contener al menos un carácter especial.")
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

        # Asignar siempre el rol de "usuario"
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
    compras = Compra.objects.filter(usuario=request.user).select_related('carrito').order_by('-fecha_compra')
    
    return render(request, 'core/perfil.html', {
        'productos': productos,
        'compras': compras
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

@require_POST
@login_required
def procesar_compra(request):
    carrito = get_object_or_404(Carrito, usuario=request.user, estado='A')
    items = CarritoProducto.objects.filter(carrito=carrito)
    if not items.exists():
        return JsonResponse({'ok': False, 'error': 'Carrito vacío'}, status=400)

    total = 0
    for item in items:
        total += item.producto.precio * item.cantidad

    compra = Compra.objects.create(
        usuario=request.user,
        carrito=carrito,
        total=total,
        metodo_pago='Transferencia'
    )
    for item in items:
        producto = item.producto
        producto.stock = F('stock') - item.cantidad
        producto.save(update_fields=['stock'])

    carrito.estado = 'C'
    carrito.save()

    return JsonResponse({'ok': True})

@login_required
def editar_perfil(request):
    user = request.user
    # Asumimos que la relación dirección ya existe o es opcional
    direccion = getattr(user, 'direccion', None)

    if request.method == 'POST':
        # Campos enviados desde el formulario
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        calle = request.POST.get('calle', '').strip()
        numero = request.POST.get('numero', '').strip()
        depto = request.POST.get('depto', '').strip() or None

        # Validaciones básicas (puedes ampliarlas)
        if not nombre or not apellido or not email:
            messages.error(request, "Nombre, apellido y email son obligatorios.")
            return redirect('perfil')
        user.nombre = nombre
        user.apellido = apellido
        user.email = email
        if password:
            user.set_password(password)
        user.save()
        if direccion:
            direccion.calle = calle or direccion.calle
            try:
                direccion.numero = int(numero)
            except ValueError:
                direccion.numero = direccion.numero
            direccion.depto = depto
            direccion.save()
        else:
            from .models import Direccion
            try:
                num = int(numero) if numero else 0
            except ValueError:
                num = 0
            direccion = Direccion.objects.create(
                calle=calle or "-",
                numero=num,
                depto=depto
            )
            user.direccion = direccion
            user.save()

        messages.success(request, "Tus datos han sido actualizados correctamente.")
        return redirect('perfil')
    
    return redirect('perfil')

@require_POST
def reset_password_request(request):
    data = json.loads(request.body)
    email = data.get('email', '').strip()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'El correo no existe.'}, status=400)
    return JsonResponse({'ok': True})

@require_POST
def reset_password_confirm(request):
    data = json.loads(request.body)
    email = data.get('email', '').strip()
    new_password = data.get('new_password', '').strip()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'El correo no existe.'}, status=400)
    user.set_password(new_password)
    user.save()
    return JsonResponse({'ok': True})