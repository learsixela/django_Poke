from abc import abstractmethod
from django.shortcuts import render, redirect
from django.contrib import messages
from login.models import User,Poke, Toque
from django.db.models import Count


# Create your views here.
def home(request):
    active_user = User.objects.get(id=request.session['user_id'])
    lista_usuarios = User.objects.all()

    #buscar donde el usuario es receptor para obtener el historial
    mis_pokes= []
    #diccionario
    los_poke=Poke.objects.filter(receptor=active_user).values('emisor').annotate(total=Count('emisor'))
    #{'emisor': 1, 'total': 1} ejemplo
    for usuario in los_poke:
        mis_pokes.append(
            {
            "emisor": User.objects.filter(id=usuario["emisor"]),#QuerySet
            "total": usuario["total"]
            }
        )
        
    # objetos de tipo poke, donde el usuario receptor es el usuario logueado
    los_poke2 = Poke.objects.filter(receptor=active_user)
    print(len(los_poke2))

    for poke in los_poke2:
        print(poke.emisor.id)

        




    context = {
        "active_user": active_user,
        "mis_pokes":mis_pokes,#arreglo de diccionarios
        "lista_usuarios" : lista_usuarios,
        "los_poke": los_poke2,
    }

    return render(request, 'home.html', context)

def addpoke(request):
    receptor = User.objects.get(id=request.POST['receptor_id'])
    emisor=User.objects.get(id=request.session['user_id'])
    receptor.historico += 1 #incrementar el historico
    receptor.save()

    Poke.objects.create(receptor=receptor, emisor=emisor)
    #toque= Toque.objects.create(receptor=receptor_id, emisor=emisor_id)

    return redirect('/home')