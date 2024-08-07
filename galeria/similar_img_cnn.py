import os
import numpy as np
import pickle
from django.conf import settings
import tensorflow as tf
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.metrics.pairwise import cosine_similarity
from galeria.util import download_image_temp
from galeria.models import ImagensCurso
from asgiref.sync import sync_to_async

# Carregar o modelo ResNet50 fora da função
resnet_model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, pooling='avg')

def extract_features(img_array):
    # Pré-processamento da imagem
    img_array = preprocess_input(img_array)
    # Extrair características (embedding) da imagem
    features = resnet_model.predict(img_array)
    return features

@sync_to_async
def save_image_features_to_db(imagem_de_ls):
    """
    Extrai as características da imagem e as salva no banco de dados como um campo binário.
    """
    image_path = download_image_temp(imagem_de_ls.imagem.url)
    img = keras_image.load_img(image_path, target_size=(224, 224))
    features = extract_features(np.expand_dims(keras_image.img_to_array(img), axis=0))

    # Serializar as características usando pickle
    features_binary = pickle.dumps(features)

    # Salvar as características no banco de dados
    imagem_de_ls.caracteristicas = features_binary
    imagem_de_ls.save()

    return np.array(features)  # Certifique-se de retornar como array NumPy

@sync_to_async
def load_image_features_from_db(imagem_de_ls):
    """
    Carrega as características da imagem a partir do banco de dados.
    """
    if imagem_de_ls.caracteristicas:
        # Deserializar as características usando pickle
        features_array = pickle.loads(imagem_de_ls.caracteristicas)
        return np.array(features_array)  # Certifique-se de retornar como array NumPy
    else:
        return None

async def find_similar_images(imagem_procurada, ls_imagens, porc_minimo_similar):
    # Extrair características da imagem de consulta
    query_image_path = download_image_temp(imagem_procurada)
    img = keras_image.load_img(query_image_path, target_size=(224, 224))
    query_features = extract_features(np.expand_dims(keras_image.img_to_array(img), axis=0))

    ls_imagens_similares = []

    for imagem_de_ls in ls_imagens:
        # Carregar ou extrair e salvar as características da imagem
        image_features = await load_image_features_from_db(imagem_de_ls)
        if image_features is None:
            image_features = await save_image_features_to_db(imagem_de_ls)

        # Calcular a similaridade usando a similaridade de cosseno entre os vetores de características
        if query_features is not None and image_features is not None:
            similaridade = cosine_similarity(query_features, image_features)[0][0]

            if (similaridade * 100 > porc_minimo_similar):
                ls_imagens_similares.append((imagem_de_ls.id, similaridade))

    # Ordenar a lista de imagens com base na similaridade (em ordem decrescente)
    ls_imagens_similares.sort(key=lambda x: x[1], reverse=True)
    
    return ls_imagens_similares

async def find_similar_2_images(imagem_procurada, imagem2):
    # Extrair características da imagem de consulta
    # print("################1")
    query_image_path = download_image_temp(imagem2)
    img = keras_image.load_img(query_image_path, target_size=(224, 224))
    query_features = extract_features(np.expand_dims(keras_image.img_to_array(img), axis=0))
    # print("################2")
    # Carregar ou extrair e salvar as características da segunda imagem
    image2_features = await load_image_features_from_db(imagem_procurada)
    if image2_features is None:
        image2_features = await save_image_features_to_db(imagem_procurada)
    # print("################3")
    # Calcular a similaridade usando a similaridade de cosseno entre os vetores de características
    if query_features is not None and image2_features is not None:
        similaridade = cosine_similarity(query_features, image2_features)[0][0]

        return similaridade * 100
    else:
        return 0
