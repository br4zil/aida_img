import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from galeria.models import ImagensCurso
from cursos.models import Cursos
from django.templatetags.static import static
from django.contrib import messages
from usuarios.views import validaAutenticacao
from galeria.forms import ImagensCursoForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

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
    
    dados_curso = {'total': 0, 'total_normal': 0, 'total_copia': 0, 'total_unicacor': 0, 'porc_normal': 0, 'porc_ida': 0, 'total_ida': 0}
    dados_curso['total'] = ImagensCurso.objects.filter(curso_id=id_curso).count()
    if(dados_curso['total']>0):
        dados_curso['total_normal'] = ImagensCurso.objects.filter(curso_id=id_curso, class_sis='Normal').count()
        dados_curso['total_ida_copia'] = ImagensCurso.objects.filter(curso_id=id_curso, class_sis='IDA Cópia').count()
        dados_curso['total_ida_mono'] = ImagensCurso.objects.filter(curso_id=id_curso, class_sis='IDA Mono').count()
        dados_curso['porc_normal'] = round(dados_curso['total_normal']/dados_curso['total']*100,2)
        total_ida = dados_curso['total_ida_copia']+dados_curso['total_ida_mono']
        dados_curso['total_ida'] = total_ida
        dados_curso['porc_ida'] = round(total_ida/dados_curso['total']*100,2)
    
    return render(request, 'galeria/index.html', {"imagens_curso":imagens_curso, "curso": curso, "dados_curso": dados_curso})



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

# @csrf_exempt
# def galeriaUpload(request):
# # Se o formulário for enviado via AJAX
#     if request.method == "POST":
#         form = ImagensCursoForm(request.POST, request.FILES)
#         c = Cursos.objects.filter(id=request.session.get('id_curso'))
#         if form.is_valid():
#             images = request.FILES.getlist('imagem')
#             total_images = len(images)
#             uploaded_images = 0
            
#             for image in images:
#                 imagem_curso = ImagensCurso(
#                     imagem=image,
#                     curso=c[0],
#                 )
#                 imagem_curso.obs_class_sis = request.build_absolute_uri()
#                 imagem_curso.save()
#                 uploaded_images += 1
                
#             # return JsonResponse({'redirect_url': reverse('galeria-list', args=[c[0].id])})
#         else:
#             errors = form.errors.as_json()
#             return JsonResponse({'errors': errors}, status=400)
#     else:
#         form = ImagensCursoForm()
#     return render(request, 'galeria/upload_imagens.html', {'form': form})




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




# def galeriaIdentificarIDA(request):
#     """
#     Sends server-sent events to the client.
#     """
#     porc_minimo_similar = 70
#     ImagensCurso.objects.filter(curso_id=1).update(class_sis=None)    
#     id_curso = request.session["id_curso"]
#     imagens = ImagensCurso.objects.order_by("id").filter(curso_id=id_curso)

#     total_de_imagens = imagens.count
#     i_imagem = 0    
#     mensagem_retorno = "Iniciando"
#     # Envia mensagem de início
#     ProgressConsumer.update_progress("Sua mensagem aqui", "progress")

     
    
#     for i, img in enumerate(imagens, start=1):
#         if(i_imagem>3):
#             break
#         i_imagem=i_imagem+1
#         mensagem_retorno = f"{i_imagem} de {total_de_imagens}"    
#         # Envia mensagem de progresso atualizado
        
      
        
#         unica_cor_imagem = unica_cor.verifica_cor_unica(img.imagem.url)
#         if unica_cor_imagem == True:
#             img.class_sis = 'IDA Mono'
#             img.save()
#         else:
#             ls_imagens = ImagensCurso.objects.order_by("id").filter(curso_id=id_curso, class_sis=None).exclude(id=img.id)
#             ls_similar_imagens = similar_img_cnn.find_similar_images(img.imagem.url, ls_imagens, porc_minimo_similar)
#             for i, (id_similiar_imagem, similaridade_imagem) in enumerate(ls_similar_imagens):
#                 # print(f"{i+1}. Similaridade com {id_similiar_imagem}: {similaridade_imagem*100:.2f}%")
#                 # print(id_similiar_imagem)
#                 imagem_atualizar_class = ImagensCurso.objects.filter(id=int(id_similiar_imagem))
#                 for i in imagem_atualizar_class:
#                     i.class_sis = "IDA Cópia"
#                     # imagem_de_ls.obs_class_sis = ', '.join(map(str, imagem_de_ls.id))
#                     i.save()
    #return redirect('/galeria-list/'+str(request.session["id_curso"]))    
    


def galeriaIdentificarIDA(request):
    messages.success(request, "Análise realizada com sucesso.")
    return redirect('/galeria-list/'+str(request.session["id_curso"]))    
    
        
      
        







# # Função de callback para atualizar o progresso
# def atualizar_progresso(mensagem):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         'progress_group',  # Nome do grupo de WebSocket
#         {
#             'type': 'update_progress',
#             'message': mensagem,
#         }
#     )  


# def galeriaIdentificarIDA(request):
#     # if not request.user.is_authenticated:
#     #     messages.error(request, "Usuário não logado.")
#     #     return redirect('login') 

#     porc_minimo_similar = 70
#     ImagensCurso.objects.filter(curso_id=1).update(class_sis=None)    
#     id_curso = request.session["id_curso"]
#     imagens = ImagensCurso.objects.order_by("id").filter(curso_id=id_curso)

#     total_de_imagens = imagens.count
#     i_imagem = 0    
#     mensagem_retorno = "Iniciando"
#     # Envia mensagem de início
#     atualizar_progresso(mensagem_retorno)        
    
#     for i, img in enumerate(imagens, start=1):
#         if(i_imagem>1):
#             break
#         i_imagem=i_imagem+1
#         mensagem_retorno = f"{i_imagem} de {total_de_imagens}"    
#         # Envia mensagem de progresso atualizado
#         atualizar_progresso(mensagem_retorno)        
        
#         unica_cor_imagem = unica_cor.verifica_cor_unica(img.imagem.url)
#         if unica_cor_imagem == True:
#             img.class_sis = 'IDA Mono'
#             img.save()
#         else:
#             ls_imagens = ImagensCurso.objects.order_by("id").filter(curso_id=id_curso, class_sis=None).exclude(id=img.id)
#             ls_similar_imagens = similar_img_cnn.find_similar_images(img.imagem.url, ls_imagens, porc_minimo_similar)
#             for i, (id_similiar_imagem, similaridade_imagem) in enumerate(ls_similar_imagens):
#                 # print(f"{i+1}. Similaridade com {id_similiar_imagem}: {similaridade_imagem*100:.2f}%")
#                 # print(id_similiar_imagem)
#                 imagem_atualizar_class = ImagensCurso.objects.filter(id=int(id_similiar_imagem))
#                 for i in imagem_atualizar_class:
#                     i.class_sis = "IDA Cópia"
#                     # imagem_de_ls.obs_class_sis = ', '.join(map(str, imagem_de_ls.id))
#                     i.save()
#     # Retorne a resposta com o progresso final
#     return HttpResponse("A análise foi concluída com sucesso!")









    # request.session['progresso'] = "fim"  
    # return JsonResponse({'mensagem': 'Tarefa finalizada'})  
    # task.status = 'COMPLETED'
    # task.save()
    # return JsonResponse({'task_id': task.id})
    # messages.success(request, "Identificação de IDA realizado com sucesso.")
    #return HttpResponse("Processamento completo")
    #return JsonResponse({'progress': 100, 'message': 'Análise concluída.'})
    
    
# def check_progress(request):
#     task_id = request.GET.get('task_id')
#     task = Task.objects.get(id=task_id)
#     return JsonResponse({
#         'status': task.status,
#         'progress': task.progress
#     })    
    
    
# def start_task(request):
#     task = Task.objects.create(name='AnalisarDA')
#     return JsonResponse({'task_id': task.id})    























# @shared_task(bind=True)
# def galeriaIdentificarIDA(request):
#     if not request.user.is_authenticated:
#         messages.error(request, "Usuário não logado.")
#         return redirect('login') 

#     porc_minimo_similar = 70
#     ImagensCurso.objects.filter(curso_id=1).update(class_sis=None)    
#     id_curso = request.session["id_curso"]
#     imagens = ImagensCurso.objects.order_by("id").filter(curso_id=id_curso)

#     total_de_imagens = imagens.count
#     i_imagem = 0    
#     task = Task.objects.create(name='AnalisarDA')
    
#     for img in imagens:
#         i_imagem=i_imagem+1
        
        
#         task.progress = i_imagem*10 #
#         task.save() #
        
        
#         # progresso = f"{i_imagem} de {total_de_imagens}"
#         # async_to_sync(channel_layer.group_send)(
#         #     'progresso', {'type': 'receber_progresso', 'progresso': progresso}
#         # )
#         unica_cor_imagem = unica_cor.verifica_cor_unica(img.imagem.url)
#         if unica_cor_imagem == True:
#             img.class_sis = 'IDA Mono'
#             img.save()
#         else:
#             ls_imagens = ImagensCurso.objects.order_by("id").filter(curso_id=id_curso, class_sis=None).exclude(id=img.id)
#             ls_similar_imagens = similar_img_cnn.find_similar_images(img.imagem.url, ls_imagens, porc_minimo_similar)
#             for i, (id_similiar_imagem, similaridade_imagem) in enumerate(ls_similar_imagens):
#                 # print(f"{i+1}. Similaridade com {id_similiar_imagem}: {similaridade_imagem*100:.2f}%")
#                 # print(id_similiar_imagem)
#                 imagem_atualizar_class = ImagensCurso.objects.filter(id=int(id_similiar_imagem))
#                 for i in imagem_atualizar_class:
#                     i.class_sis = "IDA Cópia"
#                     # imagem_de_ls.obs_class_sis = ', '.join(map(str, imagem_de_ls.id))
#                     i.save()
        
#     # request.session['progresso'] = "fim"
#     # return JsonResponse({'mensagem': 'Tarefa finalizada'})  
#     task.status = 'COMPLETED'
#     task.save()
#     return JsonResponse({'task_id': task.id})
#     # messages.success(request, "Identificação de IDA realizado com sucesso.")
#     # return redirect('/galeria-list/'+str(id_curso))


