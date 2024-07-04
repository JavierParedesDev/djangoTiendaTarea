from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'

class Persona(models.Model):
    nombre = models.CharField(max_length=30, help_text="Nombre de la persona")
    apellido = models.CharField(max_length=30, help_text="Apellido de la persona")
    email = models.EmailField(unique=True, help_text="Correo electrónico de la persona")
    contraseña = models.CharField(max_length=128, help_text="Contraseña de la persona")

    def save(self, *args, **kwargs):
        # Al guardar la contraseña, la encriptamos
        if not self.pk or 'contraseña' in self.get_dirty_fields():
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
