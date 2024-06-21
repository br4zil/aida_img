import os
from tensorflow import keras
from django.conf import settings
import numpy as np
from PIL import Image
from galeria.util import download_image_temp

def construir_modelo():
    # Defina a arquitetura do seu modelo aqui
    base_model = keras.applications.ResNet152V2(weights=None, include_top=False, input_shape=(128, 128, 3))
    x = keras.layers.GlobalAveragePooling2D()(base_model.output)
    x = keras.layers.Dense(2, activation='softmax')(x)
    modelo = keras.models.Model(inputs=base_model.input, outputs=x)
    return modelo

def classificar_imagem(url_imagem):
    nomes_classes = ['3ForaEscopo', '5Conforme']
    print("***********************")
    caminho_imagem = download_image_temp(url_imagem)
    print(url_imagem)
    print("***********************")
    
    # Carregar o modelo
    caminho_modelo = os.path.join(settings.MEDIA_ROOT, "model_class/Model_Model_ResNet152V2_weights.h5")
    
    modelo = construir_modelo()
    modelo.load_weights(caminho_modelo)
    
    # Carregar a imagem
    img = Image.open(caminho_imagem)
    img = img.convert("RGB")
    img = img.resize((128, 128))  # Certifique-se de redimensionar para o tamanho de entrada esperado pelo modelo
    img = np.array(img).astype(float)  # Normalizar pixels

    # Fazer a previsão
    img = np.expand_dims(img, axis=0)  # Adicionar dimensão de lote
    previsoes = modelo.predict(img)
    indice_classe = np.argmax(previsoes)
    
    return nomes_classes[indice_classe]
