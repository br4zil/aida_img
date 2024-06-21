import os
from tensorflow import keras
import numpy as np
from PIL import Image
from functools import lru_cache
from django.conf import settings
from galeria.util import download_image_temp
from django.core.files.storage import default_storage

class_names = ['3ForaEscopo', '5Conforme']
model = None

def carregar_modelo():
    global model
    if model is None:
        #caminho_model = os.path.join(settings.MEDIA_ROOT, "model_class", "Model_ResNet152V2.h5")
        caminho_model = os.path.join("static","model_class", "Model_ResNet152V2.h5")
        caminho_model_s3 = os.path.join(settings.MEDIA_URL, caminho_model)
        
        print("*******************")
        print(caminho_model_s3)
        if default_storage.exists(caminho_model_s3):
        #if os.path.exists(caminho_model):
            model = keras.models.load_model(caminho_model_s3)
            return True
        else:
            return False
    return True

@lru_cache(maxsize=None)
def download_and_cache_image(url):
    return download_image_temp(url)

def preprocessar_imagem(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    img = img.resize((128, 128))
    return np.array(img).astype(float)

def classificar_imagem(url_imagem):
    if carregar_modelo():
        image_path = download_and_cache_image(url_imagem)
        img = preprocessar_imagem(image_path)

        img = np.expand_dims(img, axis=0)
        predictions = model.predict(img)
        classe_index = np.argmax(predictions)
        return class_names[classe_index]
    return False










# def classificar_imagem():
#     class_names = ['3ForaEscopo', '5Conforme']
#     image_path = os.path.join(settings.MEDIA_ROOT, "atividade.jpg")
#     # Carregar o modelo
#     caminho_model = os.path.join(settings.MEDIA_ROOT, "model_class\Model_ResNet152V2.h5")

#     model = keras.models.load_model(caminho_model)
#     # Carregar a imagem
#     img = Image.open(image_path)
#     img = img.convert("RGB")
#     img = img.resize((128, 128))  # Certifique-se de redimensionar para o tamanho de entrada esperado pelo modelo
#     img = np.array(img).astype(float)  # Normalizar pixels

#     # Fazer a previsão
#     img = np.expand_dims(img, axis=0)  # Adicionar dimensão de lote
#     predictions = model.predict(img)
    
#     classe_index = np.argmax(predictions)

#     # # Decodificar previsões (para modelos treinados no ImageNet)
#     # labels = []
#     # for pred in predictions:
#     #     decoded_predictions = decode_predictions(np.expand_dims(pred, axis=0))
#     #     labels.append(decoded_predictions[0])
        
#     print('----------------------------------------------------------------------------')
#     print(class_names[classe_index])
#     print('----------------------------------------------------------------------------')    
#     #return labels

# # Uso da função:
# #resultado = classificar_imagem('/caminho/para/sua/imagem.jpg')