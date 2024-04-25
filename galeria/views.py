import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from galeria.models import ImagensCurso
from cursos.models import Cursos
from django.templatetags.static import static
from django.contrib import messages
from usuarios.views import validaAutenticacao

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


