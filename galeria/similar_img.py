import cv2
import requests
import numpy as np
from skimage.metrics import structural_similarity as ssim

def compare_images():
    # Carregar as imagens
    # imagens precisam ter a mesma dimensão
    img_url_1 = 'http://127.0.0.1:8000/media/fotos/2024/02/22/carina-nebula.png'
    img_url_2 = 'http://127.0.0.1:8000/media/fotos/2024/02/22/carina-nebula.png'
    
    response = requests.get(img_url_1, stream=True)
    imagem1_bytes = np.asarray(bytearray(response.content), dtype=np.uint8)
    img1 = cv2.imdecode(imagem1_bytes, cv2.IMREAD_COLOR)    
    
    response2 = requests.get(img_url_2, stream=True)
    imagem2_bytes = np.asarray(bytearray(response2.content), dtype=np.uint8)
    img2 = cv2.imdecode(imagem2_bytes, cv2.IMREAD_COLOR)    
    
    
    # img1 = cv2.imread('http://127.0.0.1:8000/media/fotos/2024/02/22/carina-nebula.png')
    # img2 = cv2.imread('http://127.0.0.1:8000/media/fotos/2024/02/22/carina-nebula.png')

    # Verificar se as imagens foram carregadas corretamente
    if img1 is None or img2 is None:
        print("Erro ao carregar as imagens.")
        return

    # Converter as imagens para escala de cinza
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Calcular a similaridade estrutural (SSIM)
    ssim_index = ssim(gray1, gray2)
    similarity_percent = ssim_index * 100
    print(f"***********************************Similaridade com: {similarity_percent:.2f}%")

    return ssim_index

# Imagem de referência
# reference_image = "reference_image.jpg"

# # Conjunto de imagens
# image_list = ["image1.jpg", "image2.jpg", "image3.jpg"]

# # Comparar a imagem de referência com cada imagem no conjunto
# for image in image_list:
#     similarity = compare_images(reference_image, image)
#     similarity_percent = similarity * 100  # Convertendo para porcentagem
#     print(f"Similaridade com {image}: {similarity_percent:.2f}%")
