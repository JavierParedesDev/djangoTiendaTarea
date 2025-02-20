from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto, Compra, DetalleCompra, Carrito, ItemCarrito
from .forms import AdminCreationForm, ProductoForm, DetalleCompraForm, UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import PaymentForm, ContactoForm
from django.contrib.auth.models import User
# Vistas relacionadas con el usuario y la tienda

def home(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/home.html', {'productos': productos})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')  # Redirige al dashboard de administrador si es superusuario
            else:
                return redirect('home')  # Redirige al home o a la tienda para usuarios normales
        else:
            messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')
    return render(request, 'registration/login.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False 
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}. ¡Ahora puedes iniciar sesión!')
            return redirect('login') 
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/registro.html', {'form': form})

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
    users = User.objects.all()
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # O redirige a donde desees después de crear el usuario
    else:
        form = AdminCreationForm()
    
    return render(request, 'crear_admin.html', {'form': form, 'users': users})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  # Redirige a la lista de productos después de guardar
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
    logout(request)
    return redirect('home')

# Vistas relacionadas con el carrito de compras

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.user.is_authenticated:
        # Si el usuario está autenticado, obtenemos o creamos el carrito asociado a este usuario
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    else:
        # Si el usuario no está autenticado, maneja el caso según tus requerimientos
        # Por ejemplo, podrías manejarlo sin crear un carrito si no hay usuario autenticado
        return redirect('login')  # Redirige a la página de inicio de sesión o maneja de otra forma
    
    # Creamos o actualizamos el item en el carrito
    item, item_created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not item_created:
        item.cantidad += 1
        item.save()
    
    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = get_object_or_404(Carrito, id=carrito_id)
        else:
            carrito = None
    
    items = carrito.items.all() if carrito else []
    total = sum(item.producto.precio * item.cantidad for item in items)
    
    return render(request, 'carrito.html', {'items': items, 'total': total})

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.delete()
    return redirect('ver_carrito')

# Vistas relacionadas con el proceso de pago

@login_required
def procesar_pago(request):
    carrito = obtener_carrito_usuario(request.user)
    if not carrito:
        messages.error(request, 'No hay productos en tu carrito.')
        return redirect('ver_carrito')

    total = calcular_total_carrito(carrito)

def procesar_pago(request):
    carrito = obtener_carrito_usuario(request.user)
    total = calcular_total_carrito(carrito)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Crear detalles de compra basados en los elementos del carrito
            for item in carrito.items.all():
                DetalleCompra.objects.create(
                    usuario=request.user,
                    producto=item.producto,
                    cantidad=item.cantidad
                )

            # Limpiar el carrito eliminando todos los elementos
            carrito.items.all().delete()

            # Mensaje de pago exitoso
            messages.success(request, '¡Pago exitoso! Gracias por tu compra.')
            return redirect('ver_carrito')
    else:
        form = PaymentForm()

    return render(request, 'procesar_pago.html', {'form': form, 'total': total})

def obtener_carrito_usuario(usuario):
    carrito, created = Carrito.objects.get_or_create(usuario=usuario)
    return carrito

def calcular_total_carrito(carrito):
    items = carrito.items.all()
    total = sum(item.producto.precio * item.cantidad for item in items)
    return total

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario, por ejemplo, enviando un correo electrónico
            nombre = form.cleaned_data['nombre']
            correo_electronico = form.cleaned_data['correo_electronico']
            mensaje = form.cleaned_data['mensaje']
            
            # Aquí puedes agregar la lógica para enviar el correo o guardar los datos
            # Para el propósito de este ejemplo, simplemente mostramos un mensaje de éxito
            messages.success(request, '¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.')
            return redirect('contacto')
    else:
        form = ContactoForm()
    
    return render(request, 'tienda/contacto.html', {'form': form})

def ofertas(request):
    return render(request, 'tienda/ofertas.html')
def productos(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/productos.html', {'productos': productos})