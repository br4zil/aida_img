import os
from tensorflow import keras
from django.conf import settings
import numpy as np
from PIL import Image
from tensorflow.keras.applications.imagenet_utils import decode_predictions

def classificar_imagem():
    class_names = ['3ForaEscopo', '5Conforme']
    image_path = os.path.join(settings.MEDIA_ROOT, "atividade.jpg")
    # Carregar o modelo
    caminho_model = os.path.join(settings.MEDIA_ROOT, "model_class\Model_ResNet152V2.h5")

    model = keras.models.load_model(caminho_model)
    # Carregar a imagem
    img = Image.open(image_path)
    img = img.convert("RGB")
    img = img.resize((128, 128))  # Certifique-se de redimensionar para o tamanho de entrada esperado pelo modelo
    img = np.array(img).astype(float)  # Normalizar pixels

    # Fazer a previsão
    img = np.expand_dims(img, axis=0)  # Adicionar dimensão de lote
    predictions = model.predict(img)
    
    classe_index = np.argmax(predictions)

    # # Decodificar previsões (para modelos treinados no ImageNet)
    # labels = []
    # for pred in predictions:
    #     decoded_predictions = decode_predictions(np.expand_dims(pred, axis=0))
    #     labels.append(decoded_predictions[0])
        
    print('----------------------------------------------------------------------------')
    print(class_names[classe_index])
    print('----------------------------------------------------------------------------')    
    #return labels

# Uso da função:
#resultado = classificar_imagem('/caminho/para/sua/imagem.jpg')

