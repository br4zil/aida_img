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

import requests
import tempfile
import os
import time

def download_image_temp(image_url):
    attempt = 1
    delay = 1  # Tempo inicial de espera em segundos

    while attempt <= 10:
        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code != 200:
                raise ValueError(f"Erro ao baixar a imagem {image_url}. Erro: {response.status_code}")

            # Criar um arquivo temporário para armazenar a imagem
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_url)[1]) as temp_file:
                # Gravar a imagem no arquivo temporário
                temp_file.write(response.content)
                # Retornar o caminho para o arquivo temporário
                return temp_file.name

        except Exception as e:
            print(f"Erro na tentativa {attempt}: {e}")
            if attempt == 10:
                raise e  # Relevanta a exceção se for a última tentativa
            time.sleep(delay)
            delay *= 2  # Dobra o tempo de espera
            attempt += 1


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
        with urllib.request.urlopen(image_url, timeout=10) as response:
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
    

from googletrans import Translator

def traduzir_en_pt(palavra_em_ingles: str) -> str:
    translator = Translator()
    traducao = translator.translate(palavra_em_ingles, src='en', dest='pt').text
    return traducao

def traduzir_pt_en(palavra_em_ingles: str) -> str:
    translator = Translator()
    traducao = translator.translate(palavra_em_ingles, src='pt', dest='en').text
    return traducao

# # Exemplo de uso
# palavra_em_ingles = "hello"
# palavra_em_portugues = traduzir_palavra(palavra_em_ingles)
# print(f'A tradução de "{palavra_em_ingles}" é "{palavra_em_portugues}".')
