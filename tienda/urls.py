from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'), 
    path('compras/', views.ver_compras, name='ver_compras'),
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    path('agregar-detalle-compra/', views.agregar_detalle_compra, name='agregar_detalle_compra'),
    path('lista-productos/', views.lista_productos, name='lista_productos'),
    path('eliminar-producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
]