from django.urls import path
from . import views

app_name = 'appImageA4'

urlpatterns = [
    path("", views.home, name="home"),
    path("index", views.index, name="index"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("upload", views.upload, name="upload")
]