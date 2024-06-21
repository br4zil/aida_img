from django.conf import settings
from urllib.parse import urlparse
import os

def url_to_path(url):
    """
    Recebe uma URL de uma imagem e retorna o caminho físico da imagem no sistema de arquivos.

    :param image_url: URL da imagem
    :return: Caminho físico da imagem
    """
    # Analisar a URL e obter o caminho relativo
    parsed_url = urlparse(url)
    path = parsed_url.path  # Este é o caminho relativo da URL

    # Construir o caminho físico usando MEDIA_ROOT
    image_path = os.path.join(settings.STATIC_ROOT, path.lstrip('/'))
    print(image_path)
    return image_path


import requests
import tempfile
import os

def download_image_temp(image_url):
    """
    Baixa uma imagem a partir de uma URL e armazena-a temporariamente.

    :param image_url: URL da imagem.
    :return: O caminho para o arquivo temporário onde a imagem foi armazenada.
    """
    print("***********************")
    print(image_url)
    # Fazer uma solicitação GET à URL da imagem
    response = requests.get(image_url, timeout=10)
    print("***********************")
    
    # Verificar se a resposta é bem-sucedida
    if response.status_code != 200:
        raise ValueError(f"Erro ao baixar a imagem: {response.status_code}")
    print("***********************")
    # Criar um arquivo temporário para armazenar a imagem
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_url)[1]) as temp_file:
        # Gravar a imagem no arquivo temporário
        temp_file.write(response.content)
        
        # Retornar o caminho para o arquivo temporário
        return temp_file.name

# # Exemplo de uso:
# image_url = "https://bucketaidaimg.s3.amazonaws.com/static/images/imagens_cursosLocal/1/1/12.png"
# temp_image_path = download_image_temp(image_url)
# print(f"A imagem foi baixada para: {temp_image_path}")




import urllib.request
import os
import tempfile

def download_image_temp_urllib(image_url):
    """
    Baixa uma imagem a partir de uma URL e armazena-a temporariamente usando urllib.

    :param image_url: URL da imagem.
    :return: O caminho para o arquivo temporário onde a imagem foi armazenada.
    """
    print("Starting download for:", image_url)
    try:
        with urllib.request.urlopen(image_url, timeout=30) as response:
            if response.status != 200:
                raise Exception(f"Failed to download image, status code: {response.status}")
            image_data = response.read()

        temp_dir = tempfile.gettempdir()
        print(f"Using temporary directory: {temp_dir}")

        # Verificar se o diretório temporário é acessível
        if not os.access(temp_dir, os.W_OK):
            raise PermissionError(f"Sem permissão para escrever no diretório temporário: {temp_dir}")

        file_extension = os.path.splitext(image_url)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension, dir=temp_dir) as temp_file:
            temp_file.write(image_data)
            return temp_file.name

    except urllib.error.URLError as e:
        print(f"Failed to download image: {e}")
        raise