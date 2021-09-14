from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from time import gmtime, strftime
import bcrypt

from .models import User, Poke

# Create your views here.
def login(request):
    return render(request, 'registro.html')


def registrar(request):
    return render(request, 'registro.html')


def inicio2(request):
    #capturando data desde front
    email2=request.POST['email2']
    perro=request.POST['perro']
    password=request.POST['password']

    #creacion en base datos del poke
    poke = Poke.objects.create(
        #id nunca se crea, es automatico
        email=email2,
        #email=request.POST['email2']
        perro=request.POST['perro'],
        password=request.POST['password'],
    )

    #busco desde la base datos todos los poke
    lista_pokes = Poke.objects.all()

    #return HttpResponse(email2+" "+perro+" "+password)

    #pasando data a Front   
    context={
        'gato':request.POST,
        'elefante':perro,
        'avion':password,
        'lista_pokes':lista_pokes,
    }

    return render(request, 'prueba.html',context)

def inicio(request):
    usuario = User.objects.filter(email=request.POST['email2'])
    errores = User.objects.validar_login(request.POST, usuario)

    if len(errores) > 0:
        for key, msg in errores.items():
            messages.error(request, msg)
        return redirect('/')
    else:
        request.session['user_id'] = usuario[0].id
        return redirect('home/')

def registro(request):
    #validacion de parametros
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, msg in errors.items():
            messages.error(request, msg)
        return redirect('/registrar')

    else:
        #encriptar password
        password = User.objects.encriptar(request.POST['password'])
        decode_hash_pw = password.decode('utf-8')
        
        rol = 2
        if User.objects.all().count() == 0:
            rol = 1

        #crear usuario
        user = User.objects.create(
            nombre=request.POST['nombre'],
            alias=request.POST['alias'],
            email=request.POST['email'],
            cumple=request.POST['cumple'],
            password=decode_hash_pw,
            rol=rol,
        )
        #request.session['user_id'] = user.id
        #retornar mensaje de creacion correcta
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')