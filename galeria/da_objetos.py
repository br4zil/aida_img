# import torch
# import cv2
# import numpy as np
# from galeria.util import download_image_temp
# from galeria.util import traduzir_en_pt

# def detect_objects_yolov5(imagem_url):
#     # Carregar o modelo YOLOv5 pré-treinado
#     model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

#     # Carregar a imagem
#     image_path = download_image_temp(imagem_url)
#     img = cv2.imread(image_path)

#     # Realizar detecção de objetos na imagem
#     results = model(img)

#     # Extrair os nomes das classes dos objetos detectados
#     detected_objects = []
#     for result in results.xyxy[0]:  # xyxy format
#         class_id = int(result[5])
#         class_name = model.names[class_id]
#         detected_objects.append(traduzir_en_pt(class_name))

#     return detected_objects

# # # Exemplo de uso:
# # image_path = 'caminho/para/sua/imagem.jpg'
# # detected_objects = detect_objects_yolov5(image_path)
# # print(f'Objetos detectados na imagem: {detected_objects}')
