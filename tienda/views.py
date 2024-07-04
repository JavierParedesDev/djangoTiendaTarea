from pyexpat.errors import messages
from telnetlib import LOGOUT
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto, Compra, DetalleCompra
from .forms import AdminCreationForm, ProductoForm, DetalleCompraForm
from tienda.models import Producto, Carrito, ItemCarrito

def home(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/home.html', {'productos': productos})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def ver_compras(request):
    compras = Compra.objects.filter(usuario=request.user)
    return render(request, 'tienda/ver_compras.html', {'compras': compras})

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})

@login_required
def agregar_detalle_compra(request):
    if request.method == 'POST':
        form = DetalleCompraForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.usuario = request.user
            detalle.save()
            return redirect('ver_compras')
    else:
        form = DetalleCompraForm()
    return render(request, 'agregar_detalle_compra.html', {'form': form})

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})


@login_required
def crear_admin(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # O redirige a donde desees después de crear el usuario
    else:
        form = AdminCreationForm()
    
    return render(request, 'crear_admin.html', {'form': form})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'eliminar_producto.html', {'producto': producto})

@login_required
def logout_view(request):
    LOGOUT(request)
    return redirect('home')


#carrito

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    item, item_created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not item_created:
        item.cantidad += 1
        item.save()
    return redirect('ver_carrito')

def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    total = sum(item.producto.precio * item.cantidad for item in items)
    return render(request, 'carrito.html', {'items': items, 'total': total})

def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.delete()
    return redirect('ver_carrito')

def procesar_pago(request):
    if request.method == 'POST':
        # Lógica para procesar el pago (puedes agregar la integración con un proveedor de pagos aquí)
        
        # Obtener todos los elementos del carrito para el usuario actual
        items_carrito = ItemCarrito.objects.filter(usuario=request.user)
        
        # Crear detalles de compra basados en los elementos del carrito
        for item in items_carrito:
            detalle_compra = DetalleCompra.objects.create(
                usuario=request.user,
                producto=item.producto,
                cantidad=item.cantidad
            )
        
        # Limpiar el carrito eliminando todos los elementos
        items_carrito.delete()
        
        # Mensaje de pago exitoso
        messages.success(request, '¡Pago exitoso! Gracias por tu compra.')
        
        # Redirigir a una página de confirmación o a donde desees después del pago
        return redirect('ver_carrito')  # Ajusta la URL según sea necesario
    
    # Si no es un POST, probablemente deberías manejarlo de otra manera (por ejemplo, redirigiendo a una página de error)
    return redirect('home')  # Redirige a la página de inicio o a otra página apropiada