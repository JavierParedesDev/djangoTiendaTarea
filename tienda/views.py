from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto, Compra, DetalleCompra
from .forms import AdminCreationForm, ProductoForm, DetalleCompraForm

def home(request):
    return render(request, 'tienda/home.html')

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
        form = ProductoForm(request.POST)
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
def eliminar_producto(request, producto_id):
    producto = Producto.objects.get(pk=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return redirect('lista_productos')

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
def logout_view(request):
    logout(request)
    return redirect('home')