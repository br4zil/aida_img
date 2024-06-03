# # galeria/consumers.py
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ProgressConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def update_progress(self, event):
#         progress = event['progress']
#         await self.send(text_data=str(progress))

# galeria/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio


from galeria.models import ImagensCurso
from galeria import unica_cor
from google_img_source_search import ReverseImageSearcher
from galeria import teste_google_image
from galeria import similar_img_cnn
from galeria import da_class
from asgiref.sync import sync_to_async


class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Conectar ao canal "progress"
        self.channel_name = "progress"
        await self.channel_layer.group_add('progress_group', self.channel_name)
        
        await self.channel_layer.group_add(
            self.channel_name,
            self.channel_name
        )
        await self.accept()

        porc_minimo_similar = 70
        
        #id_curso = await sync_to_async(getCursoSessao)()
        id_curso = self.scope['url_route']['kwargs']['id_curso']
        await sync_to_async(ImagensCurso.objects.filter(curso_id=id_curso).update)(class_sis=None)
        
        # Consulta assíncrona ao banco de dados usando sync_to_async
        imagens_async = ImagensCurso.objects.filter(curso_id=id_curso)
        imagens = await sync_to_async(list)(imagens_async)
        imagens_sorted = sorted(imagens, key=lambda img: img.id)

        total_de_imagens = imagens_async.count()
        i_imagem = 0    
        mensagem_retorno = "Iniciando"
        
        for i, img in enumerate(imagens, start=1):
            i_imagem += 1
            mensagem_retorno = f"{i_imagem} de {total_de_imagens}"    
            # Envia mensagem de progresso atualizado
            await self.update_progress(mensagem_retorno, self.channel_name)
            if img.class_sis==None:
                unica_cor_imagem = unica_cor.verifica_cor_unica(img.imagem.url)
                if unica_cor_imagem:
                    img.class_sis = 'IDA Mono'
                    await sync_to_async(img.save)()
                else: # DA Cópia
                    # Consulta assíncrona ao banco de dados usando sync_to_async
                    ls_imagens_async = ImagensCurso.objects.filter(curso_id=id_curso, class_sis=None).exclude(id=img.id).order_by("id")
                    ls_imagens = await sync_to_async(list)(ls_imagens_async)
                    ls_similar_imagens = similar_img_cnn.find_similar_images(img.imagem.url, ls_imagens, porc_minimo_similar)
                    
                    for id_similiar_imagem, similaridade_imagem in ls_similar_imagens:
                        # Consulta assíncrona ao banco de dados usando sync_to_async
                        imagem_atualizar_class_async = ImagensCurso.objects.filter(id=int(id_similiar_imagem))
                        imagens_atualizar_class = await sync_to_async(list)(imagem_atualizar_class_async)
                        # await sync_to_async(ImagensCurso.objects.filter(curso_id=int(id_similiar_imagem)).update)(class_sis="IDA Cópia")                  
                        for i in imagens_atualizar_class:
                            i.class_sis = "IDA Cópia"
                            await sync_to_async(i.save)()
                if img.class_sis==None:#DA Copia Web
                    rev_img_searcher = ReverseImageSearcher()
                    res_img_search = rev_img_searcher.search(img.imagem.url)
                    print(img.id)
                    if len(res_img_search)>0:
                        similaridade_imagem_web = similar_img_cnn.find_similar_2_images(img.imagem.url, res_img_search[0].image_url)
                        # print(img.id)
                        # print(img.imagem.url)
                        # print(res_img_search[0].image_url)
                        # print('------------------similar: ')
                        # print(similaridade_imagem_web)
                        if similaridade_imagem_web > 90:
                            img.class_sis = 'IDA Cópia Web'
                            await sync_to_async(img.save)()                            
                            
        await sync_to_async(ImagensCurso.objects.filter(curso_id=id_curso, class_sis=None).update)(class_sis='Normal')      
        await self.update_progress("Fim", self.channel_name)
        
        
        # for i in range(10):  # Seu laço aqui
        #     await asyncio.sleep(1)  # Simulando algum processamento
        #     # await self.send(text_data=json.dumps({'message': f'Mensagem {i}'}))
        #     await self.update_progress("teste", self.channel_name)
        #     #msg = json.dumps("{'message': f'Mensagem {i}'}")
        #     #await self.update_progress(self, msg,)




    async def disconnect(self, close_code):
        # Desconectar do canal "progress"
        await self.channel_layer.group_discard(
            self.channel_name,
            self.channel_name
        )

    async def update_progress(self, msg, channel_name):
        # Configurar o consumer para o novo canal
        self.channel_name = channel_name
        # await self.accept()
        # Enviar a mensagem
        # print("//////////////////////////////")
        await self.send(text_data=json.dumps({'message': msg}))
