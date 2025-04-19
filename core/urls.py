from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, login, registro, productos, categorias, perfil, nuevo_producto, categoria, producto

urlpatterns = [
    path('', index, name='home'),
    path('login', login, name='login'),
	path('registro', registro, name='registro'),
	path('productos', productos, name='productos'),
	path('categorias', categorias, name='categorias'),
	path('perfil', perfil, name='perfil'),
	path('productos/nuevo/', nuevo_producto, name='nuevo_producto'),
	path('categoria', categoria, name='categoria'),
	path('producto', producto, name='producto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)