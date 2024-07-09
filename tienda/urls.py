from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'), 
    path('registro/', views.registro, name='registro'),
    path('compras/', views.ver_compras, name='ver_compras'),
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    path('agregar-detalle-compra/', views.agregar_detalle_compra, name='agregar_detalle_compra'),
    path('lista-productos/', views.lista_productos, name='lista_productos'),
    path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('crear_admin/', views.crear_admin, name='crear_admin'),
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('ver-carrito/', views.ver_carrito, name='ver_carrito'),
    path('eliminar-del-carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('procesar-pago/', views.procesar_pago, name='procesar_pago'),
    path('login/', views.login_view, name='login'),
    path('editar-producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('procesar-pago/', views.procesar_pago, name='procesar_pago'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)