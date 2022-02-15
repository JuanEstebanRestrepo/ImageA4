from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from PIL import Image
from .forms import NewImageForm
from .models import UserImage

def home(request):
    return render(request, './app/home.html')

@login_required
def index(request):
    images = UserImage.objects.filter(user=request.user)
    return render(request, './app/index.html', context={'images':images})

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

@login_required
def logout_request(request):
	logout(request)
	messages.info(request, "Has cerrado sesión correctamente.") 
	return redirect("appImageA4:home")

@login_required
def upload(request):
    if request.method == "POST":
        form = NewImageForm(request.POST, request.FILES,)
        if form.is_valid():
            thought = form.save(commit=False)
            image = Image.open(thought.image)
            if image.format == "JPEG" or image.format == "JPG":
                new_image = resize_image(thought.image)
                thought.user = request.user
                thought.original_width = image.size[0]
                thought.original_height = image.size[1]
                thought.resize_width = new_image.size[0]
                thought.resize_height = new_image.size[1]
                thought.image = 'images/'+str(thought.image)
                thought.save()
                messages.success(request, "Imagen cargada correctamente." )
                loaded_image = UserImage.objects.filter(user=request.user).last()
                return redirect("appImageA4:image_detail", loaded_image.id)
            else:
                messages.error(request, "No ha sido posible cargar la imagen. Formato inválido.")
                messages.error(request, "Porfavor selecciona una imagen JPG o JPEG.")
    form = NewImageForm()
    orientation = 'horizontal'
    return render(request=request, template_name="./app/upload.html", context={'form':form, 'orientation':orientation})

def image_detail(request, pk):
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
