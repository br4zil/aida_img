from django.shortcuts import render, redirect
from usuarios.forms import LoginForms
from django.contrib import auth
from django.contrib import messages

def login(request):
    form = LoginForms()
    
    if request.method == 'POST':
        form = LoginForms(request.POST)
        if form.is_valid():
            usuario=form['usuario'].value()
            senha=form['senha'].value()
            usuario = auth.authenticate(
                request,
                username=usuario,
                password=senha
            )
        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request, f"{usuario} logado com sucesso!")
            return redirect('cursos')
            #return render(request, 'cursos/index.html', {'usuario':usuario})
            # return render(request, 'galeria/index.html', {'usuario':usuario})
            # return redirect('index', {'usuario':usuario})
        else:
            messages.error(request, "Erro ao efetuar login.")
            return redirect('login')

        
    return render(request, 'usuarios/login.html', {"form": form})


def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado.')
    return redirect('login')


def cadastro(request):
    return render(request, 'usuarios/cadastro.html')


def validaAutenticacao(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado.")
        return redirect('login') 