from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'), 
    path('compras/', views.ver_compras, name='ver_compras'),
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    path('agregar-detalle-compra/', views.agregar_detalle_compra, name='agregar_detalle_compra'),
    path('lista-productos/', views.lista_productos, name='lista_productos'),
     path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('crear_admin/', views.crear_admin, name='crear_admin'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)