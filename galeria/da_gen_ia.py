import requests
from PIL import Image
from io import BytesIO

def analisar_imagem(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança exceção se a requisição não for bem sucedida
    except requests.exceptions.RequestException as e:
        return f'Erro ao baixar a imagem: {str(e)}'
    
    try:
        img = Image.open(BytesIO(response.content))
        metadata = img.info  # Obtém os metadados da imagem
        
        # Verificar se o campo 'Software' está presente nos metadados
        software_used = metadata.get('Software', '')
        ia_generated = 'ai' in software_used.lower() or 'artificial intelligence' in software_used.lower()
        
        if ia_generated:
            return 'Esta imagem foi gerada por inteligência artificial.'
        else:
            return 'Esta imagem não foi gerada por inteligência artificial.'
        
    except Exception as e:
        return f'Erro ao analisar a imagem: {str(e)}'

# # Exemplo de uso da função:
# url_da_imagem = 'https://example.com/minha-imagem.jpg'
# resultado = analisar_imagem(url_da_imagem)
# print(resultado)










# from transformers import AutoFeatureExtractor, AutoModelForImageClassification
# from PIL import Image
# import torch
# import requests
# from io import BytesIO
# import torch.nn.functional as F

# # Carregar o extrator de características e o modelo pré-treinado
# feature_extractor = AutoFeatureExtractor.from_pretrained("microsoft/swin-tiny-patch4-window7-224")
# model = AutoModelForImageClassification.from_pretrained("microsoft/swin-tiny-patch4-window7-224")

# # Função para carregar e pré-processar a imagem
# def preprocess(image_url):
#     response = requests.get(image_url)
#     image = Image.open(BytesIO(response.content)).convert("RGB")
#     inputs = feature_extractor(images=image, return_tensors="pt")
#     return inputs

# # Função para detectar se a imagem foi gerada por IA
# def detect_image(image_url):
#     inputs = preprocess(image_url)
#     with torch.no_grad():
#         outputs = model(**inputs)
#     logits = outputs.logits
#     # Aplica a função softmax para obter as probabilidades
#     probabilidades = F.softmax(logits, dim=1)
    
#     # Obtém a classe com a maior probabilidade
#     classe_predita = torch.argmax(probabilidades, dim=1)
    
#     # Assumindo que a classe 1 representa uma imagem gerada por IA e a classe 0 uma imagem real
#     if classe_predita.item() == 1:
#         return "A imagem foi gerada por IA."
#     else:
#         return "não IA."

# # # Exemplo de uso
# # image_url = 'https://example.com/caminho_para_a_imagem.jpg'
# # resultado = detect_image(image_url)
# # print(f"A imagem é: {resultado}")
