from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from .views import index, login_view, registro, productos, categorias, perfil, nuevo_producto, categoria, producto, actualizar_producto, eliminar_producto, agregar_al_carrito, listar_carrito, modificar_cantidad_carrito, eliminar_producto_carrito

urlpatterns = [
    path('', index, name='home'),
    path('login', login_view, name='login'),
	path('registro', registro, name='registro'),
	path('productos', productos, name='productos'),
	path('categorias', categorias, name='categorias'),
	path('perfil', perfil, name='perfil'),
	path('productos/nuevo/', nuevo_producto, name='nuevo_producto'),
	path('categoria/<int:id>/', categoria, name='categoria'),
	path('producto/<int:id>/', producto, name='producto'),
    path('productos/actualizar/<int:id>/', actualizar_producto, name='actualizar_producto'),
	path('productos/eliminar/<int:id>/', eliminar_producto, name='eliminar_producto'),
    path('carrito/agregar/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/listar/', listar_carrito, name='listar_carrito'),
	path('carrito/modificar/', modificar_cantidad_carrito, name='modificar_cantidad_carrito'),
	path('carrito/eliminar/', eliminar_producto_carrito, name='eliminar_producto_carrito'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
	path('categoria/<int:id>/<slug:slug>/', categoria, name='categoria'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)