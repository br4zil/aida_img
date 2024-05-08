import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from galeria.models import ImagensCurso
from cursos.models import Cursos
from django.templatetags.static import static
from django.contrib import messages
from usuarios.views import validaAutenticacao
from galeria.forms import ImagensCursoForm


from galeria import unica_cor
from galeria import teste_google_image
from galeria import similar_img_cnn
from galeria import da_class

# DAMono unica_cor.py
# DACopia similar_img_cnn.py
# DAWeb teste_google_image.py
# DAClass da_class.py

def galeriaList(request, id_curso):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado.")
        return redirect('login') 
    imagens_curso = ImagensCurso.objects.order_by("id").filter(curso_id=id_curso)
    curso = Cursos.objects.filter(id=id_curso)
    request.session['id_curso']=curso[0].id
    request.session['nome_curso']=curso[0].nome
    return render(request, 'galeria/index.html', {"imagens_curso":imagens_curso, "curso": curso})



def galeria(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado.")
        return redirect('login') 
   
    #teste_bing_image.buscarImagem(request)
    #teste_bing.testar()
    #teste_google_image.testar()
    #similar_img.compare_images()
    
    #da_class.classificar_imagem()

    # Caminho para a imagem de consulta
    query_image_path = os.path.join(settings.MEDIA_ROOT, "carina-nebula.png")
    # Lista de caminhos para as imagens no conjunto
    image_list = [os.path.join(settings.MEDIA_ROOT, "teste.png"),
                os.path.join(settings.MEDIA_ROOT, "unicacor.png"),
                os.path.join(settings.MEDIA_ROOT, "carina-nebula.png")]
    ## Encontrar imagens semelhantes à imagem de consulta
    # similar_images = similar_img_cnn.find_similar_images(query_image_path, image_list)
    ## Imprimir os resultados
    # print("................................................................")
    # for i, (image_path, similarity) in enumerate(similar_images):
    #    print(f"{i+1}. Similaridade com {image_path}: {similarity*100:.2f}%")
    # print("----------------------------------------------------------------")       
    
    
    fotografias = ImagensCurso.objects.order_by("-data_fotografia").filter(plublicada=True)
    class_fotos = []
    imagens_google = []
    for foto in fotografias:
        arquivo = request.build_absolute_uri()[:-1];
        if foto.foto.url != '':
            arquivo = arquivo+foto.foto.url
            #print('===========================> '+arquivo)
            #imagens_google.append(teste_google_image.procurarImagem(arquivo))
        else:
            arquivo = ''
            #imagens_google.append('')
        class_fotos.append(unica_cor.verifica_cor_unica(arquivo))
    fotografias_class = zip(fotografias, class_fotos)
    
    
    
    
    return render(request, 'galeria/index.html', {"cards":fotografias_class});


def galeriaUpload(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado.")
        return redirect('login') 
    # Verifica se o método da requisição é POST
    if request.method == "POST":
        form = ImagensCursoForm(request.POST, request.FILES)
        c=Cursos.objects.filter(id=request.session.get('id_curso'))
        # Se o formulário for válido, processa as imagens
        if form.is_valid():
            # Obtenha a lista de imagens enviadas
            
            images = request.FILES.getlist('imagem')
            
            # Processa cada imagem
            for image in images:
                # Crie uma instância de ImagensCurso para cada imagem
                imagem_curso = ImagensCurso(
                    imagem=image,
                    curso=c[0],
                )
                # Salva a instância
                imagem_curso.obs_class_sis = request.build_absolute_uri()
                imagem_curso.save()
                
            # Redireciona após salvar todas as imagens
            messages.success(request, "Imagens cadastradas com sucesso.")
            return redirect('galeria-list/'+str(c[0].id))
        else:
            for field_name, error_messages in form.errors.items():
                for error in error_messages:
                    messages.error(request, f"Erro no campo {field_name}: {error}") 
    else:
        form = ImagensCursoForm()
    return render(request, 'galeria/upload_imagens.html', {'form': form})


def galeriaImagemDelete(request, id):
    imagemCurso = ImagensCurso.objects.get(id=id)
    try:
        imagemCurso.imagem.delete()
        imagemCurso.delete()
    except:
        pass
    messages.success(request, "Exclusão realizada com sucesso.")
    return redirect('/galeria-list/'+str(request.session["id_curso"]))

def galeriaImagemDeleteAll(request):
    id_curso = request.session["id_curso"]
    imagensCurso = ImagensCurso.objects.filter(curso_id=id_curso)
    try:
        for imagemCurso in imagensCurso:
            imagemCurso.imagem.delete()
            imagemCurso.delete()
    except:
        pass
    messages.success(request, "Exclusão de todas as imagens realizada com sucesso.")
    return redirect('/galeria-list/'+str(id_curso))


def galeriaIdentificarIDA(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado.")
        return redirect('login') 
    id_curso = request.session["id_curso"]
    imagens = ImagensCurso.objects.order_by("id").filter(curso_id=id_curso)
    print('------------------------------------')
    for img in imagens:
        unica_cor_imagem = unica_cor.verifica_cor_unica(img.imagem.url)
        print(unica_cor_imagem)
        if unica_cor_imagem == True:
            img.class_sis = 'IDA Mono'
            img.save()
    messages.success(request, "Identificação de IDA realizado com sucesso.")
    return redirect('/galeria-list/'+str(id_curso))