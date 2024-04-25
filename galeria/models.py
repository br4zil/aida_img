from django.db import models
from django.utils.translation import gettext_lazy as _
import os
import shutil
from django.conf import settings  # Importar as configurações do Django

def upload_to(instance, filename):
    # Define um caminho temporário para o upload inicial na pasta 'django media'
    return os.path.join(settings.MEDIA_ROOT, 'images', 'temp', filename)

class ImagensCurso(models.Model):
    NOME_IGUAL = 'IDA_igual'
    NOME_MONO = 'IDA_mono'
    NOME_COPIA = 'IDA_copia'
    NOME_COPIA_WEB = 'IDA_copia_web'
    NOME_CLASS = 'IDA_class'

    CLASS_CHOICES = [
        (NOME_IGUAL, _('IDA Igual')),
        (NOME_MONO, _('IDA Mono')),
        (NOME_COPIA, _('IDA Cópia')),
        (NOME_COPIA_WEB, _('IDA Cópia Web')),
        (NOME_CLASS, _('IDA Class')),
    ]

    nome_arquivo = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Nome do Arquivo"))
    imagem = models.ImageField(upload_to=upload_to, null=True, blank=True, verbose_name=_("Imagem"))
    curso = models.ForeignKey('cursos.Cursos', null=True, blank=True, on_delete=models.CASCADE, verbose_name=_("Curso"))
    class_sis = models.CharField(max_length=20, null=True, blank=True, choices=CLASS_CHOICES, default=NOME_IGUAL, verbose_name=_("Classificação Sistema"))
    class_prof = models.CharField(max_length=20, null=True, blank=True, choices=CLASS_CHOICES, default=NOME_IGUAL, verbose_name=_("Classificação Professor"))
    obs_class_sis = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Observações Sistema"))
    obs_class_prof = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Observações Professor"))

    def __str__(self):
        return self.nome_arquivo

    def save(self, *args, **kwargs):
        # Verifica se a instância é nova
        is_new_instance = not self.pk

        # Se for uma nova instância, salva primeiro para obter um ID
        if is_new_instance:
            super().save(*args, **kwargs)

        # Renomeia o arquivo após obter o ID
        if is_new_instance and self.imagem:
            # Armazena o nome original do arquivo
            self.nome_arquivo = os.path.basename(self.imagem.name)

            # Obtém a extensão do arquivo original
            file_extension = os.path.splitext(self.imagem.name)[-1]

            # Renomeia o arquivo para o ID da instância com a extensão original
            novo_nome_arquivo = f'{self.id}{file_extension}'

            # Define o novo caminho para o upload usando o curso, usuário, novo nome do arquivo, e a pasta django media
            novo_caminho = os.path.join(settings.MEDIA_ROOT, 'images', str(self.curso.usuario.id), str(self.curso.id), novo_nome_arquivo)

            # Caminho absoluto para o arquivo atual
            caminho_atual = self.imagem.path

            # Novo caminho absoluto para o arquivo
            novo_caminho_absoluto = novo_caminho

            # Cria diretórios se não existirem
            novo_caminho_dir = os.path.dirname(novo_caminho_absoluto)
            if not os.path.exists(novo_caminho_dir):
                os.makedirs(novo_caminho_dir)

            # Mover o arquivo para o novo caminho usando shutil.move
            shutil.move(caminho_atual, novo_caminho_absoluto)

            # Atualiza o campo de imagem com o novo caminho
            self.imagem.name = os.path.join('images', str(self.curso.usuario.id), str(self.curso.id), novo_nome_arquivo)

            # Salva novamente a instância para atualizar o caminho da imagem
            super().save(*args, **kwargs)

        else:
            # Salva a instância normalmente se não for nova
            super().save(*args, **kwargs)
