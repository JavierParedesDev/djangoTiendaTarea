from django import forms
from .models import Producto, DetalleCompra
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class AdminCreationForm(forms.ModelForm):
    
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        help_text='Ingrese una contraseña segura.'
    )
    
    confirm_password = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput,
        help_text='Ingrese la misma contraseña para verificación.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Las contraseñas no coinciden.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen']

class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad']
from django import forms

class PaymentForm(forms.Form):
    nombre = forms.CharField(label='Nombre en la tarjeta', max_length=100, required=True)
    numero_tarjeta = forms.CharField(label='Número de tarjeta', max_length=16, required=True)
    fecha_expiracion = forms.DateField(label='Fecha de expiración', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    cvv = forms.CharField(label='CVV', max_length=4, required=True, widget=forms.PasswordInput)

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre')
    correo_electronico = forms.EmailField(label='Email')
    mensaje = forms.CharField(widget=forms.Textarea, label='Mensaje')
