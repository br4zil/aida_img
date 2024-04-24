import os, requests
from django.templatetags.static import static
from azure.cognitiveservices.search.imagesearch import ImageSearchClient
from msrest.authentication import CognitiveServicesCredentials
from django.conf import settings


def buscarImagem(request):
    # Sua chave de assinatura
    subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']

    # URL da API de Pesquisa Visual do Bing
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/details"

   # Caminho da imagem dentro do seu projeto Django
    image_relative_path = "assets/logo/Logo(2).png"

    # Caminho absoluto do arquivo estático usando a função static()
    image_path = os.path.join(settings.STATIC_ROOT, image_relative_path)

    # Cabeçalhos com a chave de assinatura
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}

    # Parâmetros do pedido de pesquisa
    params = {"modules": "All"}

    # Ler a imagem local
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Fazer a chamada para a API
    response = requests.post(search_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    search_results = response.json()

    # Processar os resultados (por exemplo, exibir informações sobre a imagem)
    print(search_results)
