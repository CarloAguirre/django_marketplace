from django.urls import path
from .views import lista_productos, producto_detalle
from .viewsLogin import login

urlpatterns = [
    path('productos/', lista_productos, name='lista-productos'),
    path('productos/<int:pk>/', producto_detalle, name='producto-detalle'),
	path('auth/', login, name='api-login')
	
]
