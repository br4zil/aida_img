from django.shortcuts import render, redirect
from datetime import datetime
from cursos.models import Cursos
from django.contrib import messages
from cursos.forms import CursosForm
from usuarios.views import validaAutenticacao

def cursos(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado.")
        return redirect('login') 
    usuario_logado = request.user
    cursos = Cursos.objects.filter(usuario=usuario_logado).order_by("-id")
    return render(request, 'cursos/index.html', {"cursos": cursos});


def cursosUpdate(request, id):
    curso = Cursos.objects.get(id=id)
    form = CursosForm(initial={
        'nome': curso.nome, 'professor': curso.professor, 'data': curso.data, 
        'instituicao': curso.instituicao, 'usuario': curso.usuario
    })
    if request.method == "POST":  
        form = CursosForm(request.POST, instance=curso)  
        if form.is_valid():  
            try:  
                form.save() 
                model = form.instance
                return redirect('cursos')  
            except Exception as e: 
                pass   
        else:
            for field_name, error_messages in form.errors.items():
                for error in error_messages:
                    messages.error(request, f"Erro no campo {field_name}: {error}") 
    return render(request,'cursos/cursos-update.html',{'form':form})  


def cursosCreate(request):  
    if request.method == "POST":  
        form = CursosForm(request.POST)
        form_data = form.data.copy()
        form_data['data'] = datetime.now().date().isoformat()
        form_data['usuario'] = request.user.id
        form = CursosForm(form_data)

        if form.is_valid():  
            try:  
                form.save() 
                model = form.instance
                return redirect('cursos')  
            except:
                pass
        else:
            for field_name, error_messages in form.errors.items():
                for error in error_messages:
                    messages.error(request, f"Erro no campo {field_name}: {error}") 
    else:  
        form = CursosForm()  
    return render(request,'cursos/cursos-create.html',{'form':form})  




def cursosDelete(request, id):
    curso = Cursos.objects.get(id=id)
    try:
        curso.delete()
    except:
        pass
    return redirect('cursos')