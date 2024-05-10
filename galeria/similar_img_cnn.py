import os
import numpy as np
from django.conf import settings
import tensorflow as tf
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.metrics.pairwise import cosine_similarity
from galeria.util import url_to_path, download_image_temp

def extract_features(image_path):
    # Carregar e pré-processar a imagem
    img = keras_image.load_img(image_path, target_size=(224, 224))
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Carregar o modelo ResNet50 pré-treinado sem a camada final
    model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, pooling='avg')

    # Extrair as características (embedding) da imagem
    features = model.predict(img_array)

    return features



def find_similar_images(imagem_procurada, ls_imagens, porc_minimo_similar):
    # Extrair características da imagem de consulta
    # print('xxxxxxxxxxxxxx')    
    query_features = extract_features(download_image_temp(imagem_procurada))
    

    ls_imagens_similares = []

    # Calcular a similaridade entre a imagem de consulta e cada imagem na lista
    for imagem_de_ls in ls_imagens:
        image_features = extract_features(download_image_temp(imagem_de_ls.imagem.url))

        # Calcular a similaridade usando a similaridade de cosseno entre os vetores de características
        similaridade = cosine_similarity(query_features.reshape(1, -1), image_features.reshape(1, -1))[0][0]

        if (similaridade*100>porc_minimo_similar):
        # Adicionar a similaridade e o caminho da imagem à lista
            ls_imagens_similares.append((imagem_de_ls.id, similaridade))

    # Ordenar a lista de imagens com base na similaridade (em ordem decrescente)
    ls_imagens_similares.sort(key=lambda x: x[1], reverse=True)
    # print('////////////////////////////')    
    # for i, (image_path, similarity) in enumerate(ls_imagens_similares):
    #     print(f"{i+1}. Similaridade com {image_path}: {similarity*100:.2f}%")
    return ls_imagens_similares


