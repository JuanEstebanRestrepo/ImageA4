from django.urls import path, re_path
from . import views

app_name = 'appImageA4'

urlpatterns = [
    path("", views.home, name="home"),
    path("index", views.index, name="index"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("upload", views.upload, name="upload"),
    re_path(r'^image_detail/(?P<pk>\d+)$', views.image_detail, name="image_detail"),
]