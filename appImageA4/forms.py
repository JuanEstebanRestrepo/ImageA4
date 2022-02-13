from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserImage


# Create your forms here.

class NewUserForm(UserCreationForm):
    username = forms.CharField(required=True, label="Usuario")
    email = forms.EmailField(required=True, label="Correo electrónico")
    password1 = forms.CharField(required=True, label="Contraseña")
    password2 = forms.CharField(required=True, label="Verificar contraseña")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class NewImageForm(forms.ModelForm):
    name = forms.CharField(required=True, label="Nombre")
    description = forms.CharField(required=True, label="Descripción")
    image = forms.ImageField(required=True, label="Seleccionar imagen")

    class Meta:
        model = UserImage
        fields = ("name", "description", "image")