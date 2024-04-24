import os
import cv2
import numpy as np
import requests
from django.templatetags.static import static
from django.conf import settings


def verifica_cor_unica(imagemUrl):
    
    #x = 'C:/Users/gilso/Downloads/not-found.png'
    #caminho_imagem = os.path.join(settings.MEDIA_URL, imagemUrl)
    
    response = requests.get(imagemUrl, stream=True)
    if response.status_code == 200:
        imagem_bytes = np.asarray(bytearray(response.content), dtype=np.uint8)
        imagem = cv2.imdecode(imagem_bytes, cv2.IMREAD_COLOR)
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    
        # Calcula o histograma da imagem
        hist = cv2.calcHist([imagem_cinza], [0], None, [256], [0,256])
    
        # Verifica se há um único pico no histograma
        num_picos = np.sum(hist > 0)
    
        # Se houver apenas um pico, a imagem possui apenas uma cor predominante
        if num_picos == 1:
            return True
        else:
            return False
    
    return False

# # Carrega a imagem
# imagem = cv2.imread('exemplo.jpg')

# # Verifica se a imagem possui apenas uma cor predominante
# cor_unica = verifica_cor_unica(imagem)

# # Exibe o resultado
# if cor_unica:
#     print("A imagem possui apenas uma cor predominante.")
# else:
#     print("A imagem possui mais de uma cor predominante.")