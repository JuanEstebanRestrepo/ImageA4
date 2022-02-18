from django.shortcuts import  render, redirect
from ..forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_http_methods, require_safe

@require_http_methods(["GET", "POST"])
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Ha sido registrado correctamente." )
			return redirect("appImageA4:index")
		messages.error(request, "No ha sido posible registrarlo. Información inválida.")
	form = NewUserForm()
	return render (request=request, template_name="./registration/register.html", context={"register_form":form})

@require_http_methods(["GET", "POST"])
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"Has iniciado sesión como {username}.")
				return redirect("appImageA4:index")
			else:
				messages.error(request,"Usuario o contraseña inválidos.")
		else:
			messages.error(request,"Usuario o contraseña inválidos.")

	form = AuthenticationForm()
	return render(request=request, template_name="./registration/login.html", context={"login_form":form})

@require_safe
def logout_request(request):
	if request.user.is_authenticated:
		logout(request)
		messages.info(request, "Has cerrado sesión correctamente.") 
		return redirect("appImageA4:home")
	else:
		messages.error(request, "No has iniciado sesión.") 
		return redirect("appImageA4:home")