from abc import abstractmethod
from django.shortcuts import render, redirect
from django.contrib import messages
from login.models import User


# Create your views here.
def home(request):
    asd = User.objects.get(id=request.session['user_id'])
    lista_usuarios = User.objects.all()

    #buscar donde el usuario es receptor para obtener el historial

    context = {
        "active_user": asd,
        "lista_usuarios" : lista_usuarios
    }

    return render(request, 'home.html', context)
