import os
from tensorflow import keras
import numpy as np
from PIL import Image
from functools import lru_cache
from django.conf import settings
from galeria.util import download_image_temp
from django.core.files.storage import default_storage
import hashlib
import boto3
import requests
from botocore.exceptions import ClientError

class_names = ['3ForaEscopo', '5Conforme']
model = None

def get_s3_file_metadata(bucket_name, key):
    s3 = boto3.client('s3')
    try:
        response = s3.head_object(Bucket=bucket_name, Key=key)
        return response['ETag'], response['ContentLength']
    except ClientError as e:
        print(f"Erro ao obter metadados do arquivo S3: {e}")
        return None, None

def baixar_arquivo_s3(url, local_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)  # Criar o diretório se não existir
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    return False

def calcular_etag(local_file_path):
    hash_md5 = hashlib.md5()
    with open(local_file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return f'"{hash_md5.hexdigest()}"'

def carregar_modelo():
    global model
    if model is None:
        bucket_name = 'bucketaidaimg'
        key = 'static/model_class/Model_ResNet152V2.h5'
        caminho_model_s3 = f"https://{bucket_name}.s3.amazonaws.com/{key}"
        local_file_path = os.path.join(settings.MEDIA_ROOT, 'model_class', 'Model_ResNet152V2.h5')
        
        print("*******************")
        print(caminho_model_s3)

        # Obter metadados do arquivo no S3
        s3_etag, s3_file_size = get_s3_file_metadata(bucket_name, key)
        if s3_etag is None or s3_file_size is None:
            print("Erro ao obter metadados do arquivo no S3.")
            return False

        # Verificar se o arquivo já existe localmente e tem o mesmo tamanho e ETag
        if os.path.exists(local_file_path):
            local_file_size = os.path.getsize(local_file_path)
            local_etag = calcular_etag(local_file_path)
            
            if local_file_size == s3_file_size and local_etag == s3_etag:
                print("Arquivo já existe localmente e não foi modificado.")
                model = keras.models.load_model(local_file_path)
                return True
            else:
                print("Arquivo local difere do arquivo no S3. Baixando novamente.")

        # Baixar o arquivo do S3
        if baixar_arquivo_s3(caminho_model_s3, local_file_path):
            model = keras.models.load_model(local_file_path)
            print(f"Modelo carregado com sucesso a partir de {caminho_model_s3}")
            return True
        else:
            print(f"Falha ao baixar o modelo de {caminho_model_s3}")
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