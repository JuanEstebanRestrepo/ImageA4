from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_safe
from PIL import Image
from .forms import NewImageForm
from .models import UserImage

@require_safe
def home(request):
	return render(request, './app/home.html')

@login_required
@require_safe
def index(request):
	images = UserImage.objects.filter(user=request.user)
	return render(request, './app/index.html', context={'images':images})

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


@login_required
@require_http_methods(["GET", "POST"])
def upload(request):
	if request.method != "GET":
		form = NewImageForm(request.POST, request.FILES)
		files = request.FILES.getlist('image')
		loaded_image = None
		if form.is_valid():
			thought = form.save(commit=False)
			consecutive = 0
			name = thought.name
			for file in files:
				image = Image.open(file)
				if image.format == "JPEG" or image.format == "JPG":
					new_name = name if consecutive == 0 else name+str(consecutive)
					file_name = file.name
					file.name = verify_file_name(file_name)
					new_image = resize_image(file)
					UserImage.objects.create(
						user = request.user,
						name = new_name,
						description = thought.description,
						original_width = new_image.size[0],
						original_height = new_image.size[1],
						resize_width = new_image.size[0],
						resize_height = new_image.size[1],
						image = 'images/'+str(file.name)
					)
					messages.success(request, "Imagen "+file.name+" cargada correctamente." )
					loaded_image = UserImage.objects.filter(user=request.user).last()
				else:
					messages.error(request, "No ha sido posible cargar la imagen "+file.name+" . Formato inválido.")
					messages.error(request, "Porfavor selecciona una imagen JPG o JPEG.")
				consecutive += 1
		else: 
			messages.error(request, "No ha sido posible cargar la imagen. Formato inválido.")
			messages.error(request, "Porfavor selecciona una imagen JPG o JPEG.")

		if loaded_image != None:
			return redirect("appImageA4:image_detail", loaded_image.id)
	form = NewImageForm()
	orientation = 'horizontal'
	return render(request=request, template_name="./app/upload.html", context={'form':form, 'orientation':orientation})

def verify_file_name(file_name):
	file_name_com = file_name
	consecutivo_copia = 0
	verify_name = 'diferent'
	while verify_name != None:
		verify_name = UserImage.objects.filter(image='images/'+file_name_com).first()
		if verify_name != None:
			consecutivo_copia += 1
			file_name_com = '(copia'+str(consecutivo_copia)+')'+file_name
		elif consecutivo_copia == 0:
			consecutivo_copia = 0
		else:
			file_name = '(copia'+str(consecutivo_copia)+')'+file_name
	return file_name

def image_detail(request, pk):
	print('request: ', request)
	orientation = 'horizontal'
	loaded_image = UserImage.objects.filter(id = pk, user=request.user).first()
	if(loaded_image != None):
		image = Image.open(loaded_image.image)
		width = image.size[0]
		height = image.size[1]
		orientation = check_orientation(width, height)
		return render(request=request, template_name="./app/image.html", context={'loaded_image':loaded_image, 'orientation':orientation})
	else:
		return render(request=request, template_name="./app/image.html", context={'orientation':orientation})

bigA4 = 1123
littleA4 = 796
def resize_image(thought):
	image = Image.open(thought)
	width = image.size[0]
	height = image.size[1]
	check_bigger_size = check_size(width, height)
	if(check_bigger_size == True):
		orientation = check_orientation(width, height)
		if(orientation == 'horizontal'):
			image.thumbnail((bigA4, littleA4))
		else:
			image.thumbnail((littleA4, bigA4))
	image.save('media/images/'+str(thought), image.format)
	return image

def check_size(width, height):
	if(width > littleA4 or height > littleA4):
		return True
	else:
		return False

def check_orientation(width, height):
	if(width >= height):
		return 'horizontal' 
	else:
		return 'vertical'
