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
			messages.success(request, "Registration successful." )
			return redirect("appImageA4:index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
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
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("appImageA4:index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="./registration/login.html", context={"login_form":form})

@login_required
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("appImageA4:login")

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
        return redirect("appImageA4:upload")
    form = NewImageForm()
    orientation = 'horizontal'
    loaded_image = UserImage.objects.last()
    print('------------', loaded_image)
    if(loaded_image != None):
        image = Image.open(loaded_image.image)
        width = image.size[0]
        height = image.size[1]
        orientation = check_orientation(width, height)
        return render(request=request, template_name="./app/upload.html", context={'form':form, 'loaded_image':loaded_image, 'orientation':orientation})
    else:
        return render(request=request, template_name="./app/upload.html", context={'form':form, 'orientation':orientation})

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
