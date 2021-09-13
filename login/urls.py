from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login),
    path('registrar', views.registrar),
    path('login', views.inicio),
    path('registros', views.registro),
    path('logout', views.logout),
]