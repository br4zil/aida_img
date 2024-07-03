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
from django.db import transaction
from galeria.models import ImagensCurso
from cursos.models import Cursos
from galeria import unica_cor, similar_img_cnn, da_class, da_objetos, da_clip
from galeria.util import traduzir_pt_en, traduzir_en_pt
from google_img_source_search import ReverseImageSearcher

from asgiref.sync import sync_to_async

class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_name = "progress"
        await self.channel_layer.group_add('progress_group', self.channel_name)
        await self.accept()

        porc_minimo_similar = 70
        id_curso = self.scope['url_route']['kwargs']['id_curso']
        checkbox_ia = self.scope['url_route']['kwargs']['checkbox_ia']

        # Atualizar todas as imagens do curso para class_sis=None de forma assíncrona
        await sync_to_async(ImagensCurso.objects.filter(curso_id=id_curso).update)(class_sis=None)

        # Carregar dados do curso
        cursos_async = Cursos.objects.filter(id=id_curso)
        curso = await sync_to_async(list)(cursos_async)
        ls_descricao_esperada_imagens = []
        # Verificar se o curso foi encontrado
        if curso:
            if curso[0].imagens_esperadas != None:
                imagens_esperadas = curso[0].imagens_esperadas
                imagens_esperadas_en = traduzir_pt_en(imagens_esperadas)
                ls_descricao_esperada_imagens = imagens_esperadas_en.split(',')
                
        

        # Carregar todas as imagens do curso em lotes
        imagens_async = ImagensCurso.objects.filter(curso_id=id_curso)
        imagens = await sync_to_async(list)(imagens_async)
        total_de_imagens = imagens_async.count()
        erro=""

        for i, img in enumerate(imagens, start=1):
            # Atualizar progresso
            await self.update_progress(f"{i} de {total_de_imagens} {erro}", self.channel_name)

            # # DA objetos
            # objetos_detectados = da_objetos.detect_objects_yolov5(img.imagem.url)
            # print("=====================================================")
            # for objeto in objetos_detectados:
            #     print(f'Objetos detectados na imagem: {objeto}')


            # Verificar se a imagem tem uma cor única
            unica_cor_imagem = unica_cor.verifica_cor_unica(img.imagem.url)
            if unica_cor_imagem:
                img.class_sis = 'IDA Mono'
                await sync_to_async(img.save)()
            else:
                # Encontrar imagens similares na base de dados local
                ls_imagens_async = ImagensCurso.objects.filter(curso_id=id_curso, class_sis=None).exclude(id=img.id).order_by("id")
                ls_imagens = await sync_to_async(list)(ls_imagens_async)
                ls_similar_imagens = similar_img_cnn.find_similar_images(img.imagem.url, ls_imagens, porc_minimo_similar)

                for id_similar_imagem, _ in ls_similar_imagens:
                    imagem_atualizar_class_async = ImagensCurso.objects.filter(id=int(id_similar_imagem))
                    imagens_atualizar_class = await sync_to_async(list)(imagem_atualizar_class_async)
                    for i in imagens_atualizar_class:
                        i.class_sis = "IDA Cópia"
                        await sync_to_async(i.save)()

                # Se não encontrou similar na base local, buscar na web
                if img.class_sis is None:
                    rev_img_searcher = ReverseImageSearcher()
                    res_img_search = rev_img_searcher.search(img.imagem.url)
                    if res_img_search and similar_img_cnn.find_similar_2_images(img.imagem.url, res_img_search[0].image_url) > 90:
                        img.class_sis = 'IDA Cópia Web'
                        await sync_to_async(img.save)()

                # Se ainda não classificada, classificar usando o modelo da_class
                if img.class_sis is None and checkbox_ia=='s':
                    classificacao = da_class.classificar_imagem(img.imagem.url)
                    if classificacao == False:
                        erro="(Erro: Modelo IA não carregado)"
                    else:
                        erro=""
                        if classificacao == '3ForaEscopo':
                            img.class_sis = 'IDA Class'
                            await sync_to_async(img.save)()

                
                # DA Clip
                if len(ls_descricao_esperada_imagens) > 0:
                    if img.class_sis is None:
                        #string = traduzir_pt_en("desenho de um cachorro em uma camiseta")
                        photo_objects = da_clip.get_image_objects(img.imagem.url, ls_descricao_esperada_imagens)
                        print("=====================================================")
                        print("Resultados para a foto:")
                        print(img.imagem.url)
                        for obj, prob in photo_objects:
                            print(f"{obj}: {prob:.4f}")
                            if obj in imagens_esperadas_en and prob>=0.9:
                                img.class_sis = 'Normal Esperado'
                                await sync_to_async(img.save)()

        # Atualizar as imagens restantes do curso para class_sis='Normal'
        await sync_to_async(ImagensCurso.objects.filter(curso_id=id_curso, class_sis=None).update)(class_sis='Normal')

        # Finalizar e enviar mensagem de conclusão
        await self.update_progress("Fim", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.channel_name, self.channel_name)

    async def update_progress(self, msg, channel_name):
        self.channel_name = channel_name
        await self.send(text_data=json.dumps({'message': msg}))

