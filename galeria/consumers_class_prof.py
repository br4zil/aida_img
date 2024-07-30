import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from galeria.models import ImagensCurso

class UpdateConsumerClassProf(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        imagem_id = data['imagem_id']
        class_prof = data['class_prof']
        
        # Use sync_to_async para fazer chamadas ORM
        imagem_curso = await sync_to_async(ImagensCurso.objects.get)(id=imagem_id)
        imagem_curso.class_prof = class_prof
        await sync_to_async(imagem_curso.save)()

        # Envie a resposta de volta ao cliente
        await self.send(text_data=json.dumps({
            'status': 'success',
            'message': 'Atualização realizada com sucesso!',
            'imagem_id': imagem_id
        }))
