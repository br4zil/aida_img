# import torch
# from PIL import Image
# import requests
# from io import BytesIO
# from transformers import CLIPProcessor, CLIPModel

# def get_image_objects(image_url, custom_descriptions=None):
#     # Carrega o modelo e o processador CLIP da Hugging Face
#     model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
#     processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    
#     try:
#         # Baixa a imagem da URL
#         response = requests.get(image_url)
#         response.raise_for_status()  # Levanta um erro para respostas inválidas
#         image = Image.open(BytesIO(response.content)).convert("RGB")
#     except (requests.exceptions.RequestException, UnidentifiedImageError) as e:
#         print(f"Erro ao baixar ou identificar a imagem: {e}")
#         return []
    
#     # Lista de descrições de objetos comuns em inglês
#     descriptions = [
#         "a photo of a cat", "a photo of a dog", "a photo of a car",
#         "a drawing of a cat", "a drawing of a dog", "a drawing of a car",
#         "a painting of a tree", "a painting of a person", "a drawing of a bicycle",
#         "a drawing of a building", "a drawing of food", "a drawing of a book",
#         "a drawing of a chair", "a drawing of a computer", "a drawing of a phone",
#         "a drawing of a bag", "a drawing of shoes", "a drawing of clothes"
#     ]
    
#     if custom_descriptions:
#         descriptions.extend(custom_descriptions)
    
#     # Prepara as entradas do modelo
#     inputs = processor(text=descriptions, images=image, return_tensors="pt", padding=True)
    
#     # Realiza a inferência com o modelo CLIP
#     outputs = model(**inputs)
    
#     # Calcula as similaridades
#     logits_per_image = outputs.logits_per_image
#     probs = logits_per_image.softmax(dim=1)  # Obtém as probabilidades
    
#     # Encontra os índices das descrições com maior similaridade
#     best_matches = torch.topk(probs, k=1, dim=1)  # Retorna as top 5 descrições mais prováveis
#     best_indices = best_matches.indices[0]
#     best_probs = best_matches.values[0]
    
#     # Retorna as descrições dos objetos encontrados na imagem
#     results = [(descriptions[idx], prob.item()) for idx, prob in zip(best_indices, best_probs)]
    
#     return results




# # Exemplo de uso com uma foto
# photo_url = "https://example.com/photo.jpg"
# photo_objects = get_image_objects(photo_url)
# print("Resultados para a foto:")
# for obj, prob in photo_objects:
#     print(f"{obj}: {prob:.4f}")

# # Exemplo de uso com um desenho
# drawing_url = "https://example.com/drawing.jpg"
# drawing_objects = get_image_objects(drawing_url)
# print("\nResultados para o desenho:")
# for obj, prob in drawing_objects:
#     print(f"{obj}: {prob:.4f}")
