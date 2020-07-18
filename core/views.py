from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.http.response import JsonResponse

#O redirecionamento vai ser feito na url
# def index(request):
#     return redirect('/agenda/')

def login_user(request):
    return render(request,'login.html')

def submitLogin(request):
    if(request.POST):
        user = request.POST.get('user')
        password = request.POST.get('pass')
        usuario = authenticate(username=user, password=password)

        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request,'Usuario ou senha invalido')
    return redirect('/login/')

def logout_user(request):
    logout(request)
    return redirect('/')


@login_required(login_url = '/login/')
def lista_eventos(request):
    #evento = Evento.objects.get(id = 1)
    #evento = Evento.objects.all()
    #usuario só pode ver seus eventos
    usuario = request.user
    data = datetime.now()
    #evento = Evento.objects.filter(usuario=usuario)
    evento = Evento.objects.filter(usuario=usuario,data_evento__gt=data)#__gt > e __lt <
    response = {'eventos': evento}
    return render(request,"agenda.html",response)

@login_required(login_url = '/login/')
def evento(request):
    id = request.GET.get('id')
    dados = {}
    if id:
        dados['evento'] = Evento.objects.get(id=id)
    return render(request, 'evento.html', dados)

@login_required(login_url = '/login/')
def submitEvento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data = request.POST.get('data')
        desc = request.POST.get('descricao')
        user = request.user
        id = request.POST.get('id')
        if id:
            Evento.objects.filter(id=id).update(
                titulo = titulo,
                data_evento = data,
                descricao = desc,
                usuario = user
            )
        else:
            Evento.objects.create(
                titulo = titulo,
                data_evento = data,
                descricao = desc,
                usuario = user
            )
    return redirect('/')

@login_required(login_url = '/login/')
def deleteEvento(request,id):
    #Evento.objects.filter(id=id).delete()
    user = request.user
    evento = Evento.objects.get(id=id)
    if user == evento.usuario:
        evento.delete()
    return redirect('/')

@login_required(login_url = '/login/')
def jsonEvento(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario).values('id','titulo')
    return JsonResponse(list(evento),safe=False)#safe pois estou retornando lista nao dicionario {}