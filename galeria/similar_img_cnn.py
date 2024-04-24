import os
import numpy as np
from django.conf import settings
import tensorflow as tf
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.metrics.pairwise import cosine_similarity

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

def find_similar_images(query_image_path, image_list):
    # Extrair características da imagem de consulta
    query_features = extract_features(query_image_path)

    similar_images = []

    # Calcular a similaridade entre a imagem de consulta e cada imagem na lista
    for image_path in image_list:
        image_features = extract_features(image_path)

        # Calcular a similaridade usando a similaridade de cosseno entre os vetores de características
        similarity = cosine_similarity(query_features.reshape(1, -1), image_features.reshape(1, -1))[0][0]

        # Adicionar a similaridade e o caminho da imagem à lista
        similar_images.append((image_path, similarity))

    # Ordenar a lista de imagens com base na similaridade (em ordem decrescente)
    similar_images.sort(key=lambda x: x[1], reverse=True)

    return similar_images


