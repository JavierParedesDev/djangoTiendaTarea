from django import forms
from .models import Producto, DetalleCompra
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        fields = ['nombre', 'descripcion', 'precio', 'stock']

class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad']
