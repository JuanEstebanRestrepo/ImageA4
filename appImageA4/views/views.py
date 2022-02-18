from django.shortcuts import  render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe
from ..models import UserImage

@require_safe
def home(request):
	return render(request, './app/home.html')

@login_required
@require_safe
def index(request):
	images = UserImage.objects.filter(user=request.user)
	return render(request, './app/index.html', context={'images':images})