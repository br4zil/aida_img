import os
import numpy as np
from django.conf import settings
import tensorflow as tf
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.metrics.pairwise import cosine_similarity
from galeria.util import url_to_path, download_image_temp

# Carregar o modelo ResNet50 fora da função
resnet_model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, pooling='avg')

def extract_features(img_array):
    # Pré-processamento da imagem
    img_array = preprocess_input(img_array)
    # Extrair características (embedding) da imagem
    features = resnet_model.predict(img_array)
    return features

def find_similar_images(imagem_procurada, ls_imagens, porc_minimo_similar):
    # Extrair características da imagem de consulta
    query_image_path = download_image_temp(imagem_procurada)
    img = keras_image.load_img(query_image_path, target_size=(224, 224))
    query_features = extract_features(np.expand_dims(keras_image.img_to_array(img), axis=0))

    ls_imagens_similares = []

    # Pré-calcular características de todas as imagens em ls_imagens
    image_features_cache = {}
    for imagem_de_ls in ls_imagens:
        image_path = download_image_temp(imagem_de_ls.imagem.url)
        img = keras_image.load_img(image_path, target_size=(224, 224))
        image_features_cache[imagem_de_ls.id] = extract_features(np.expand_dims(keras_image.img_to_array(img), axis=0))

    # Calcular a similaridade entre a imagem de consulta e cada imagem na lista
    for imagem_de_ls in ls_imagens:
        image_features = image_features_cache[imagem_de_ls.id]

        # Calcular a similaridade usando a similaridade de cosseno entre os vetores de características
        similaridade = cosine_similarity(query_features, image_features)[0][0]

        if (similaridade*100 > porc_minimo_similar):
            # Adicionar a similaridade e o caminho da imagem à lista
            ls_imagens_similares.append((imagem_de_ls.id, similaridade))

    # Ordenar a lista de imagens com base na similaridade (em ordem decrescente)
    ls_imagens_similares.sort(key=lambda x: x[1], reverse=True)
    
    return ls_imagens_similares


def find_similar_2_images(imagem_procurada, imagem2):
    # Extrair características da imagem de consulta
    query_image_path = download_image_temp(imagem_procurada)
    img = keras_image.load_img(query_image_path, target_size=(224, 224))
    query_features = extract_features(np.expand_dims(keras_image.img_to_array(img), axis=0))

    ls_imagens_similares = []

    # Pré-calcular características de todas as imagens em ls_imagens
    image_features_cache = {}
    #for imagem_de_ls in ls_imagens:
    image_path = download_image_temp(imagem2)
    img = keras_image.load_img(image_path, target_size=(224, 224))
    image_features_cache = extract_features(np.expand_dims(keras_image.img_to_array(img), axis=0))

    # Calcular a similaridade entre a imagem de consulta e cada imagem na lista
    #for imagem_de_ls in ls_imagens:
    image_features = image_features_cache

    # Calcular a similaridade usando a similaridade de cosseno entre os vetores de características
    similaridade = cosine_similarity(query_features, image_features)[0][0]

    #if (similaridade*100 > porc_minimo_similar):
        # Adicionar a similaridade e o caminho da imagem à lista
#        ls_imagens_similares.append((imagem_de_ls.id, similaridade))

    # Ordenar a lista de imagens com base na similaridade (em ordem decrescente)
    #ls_imagens_similares.sort(key=lambda x: x[1], reverse=True)
    
    return similaridade*100
