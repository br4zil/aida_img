from django.db import models
from django.utils.translation import gettext_lazy as _

def upload_to(instance, filename):
    # Extrai a extensão do arquivo original
    file_extension = filename.split('.')[-1]
    # Renomeia o arquivo para o ID da instância e mantém a extensão original
    novo_nome_arquivo = f'{instance.id}.{file_extension}'
    # Define o caminho para o upload usando o nome do curso e o novo nome do arquivo
    caminho = f'images/{instance.curso.nome}/{novo_nome_arquivo}'
    return caminho

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

    nome_arquivo = models.CharField(max_length=255, verbose_name=_("Nome do Arquivo"))
    imagem = models.ImageField(upload_to=upload_to, verbose_name=_("Imagem"))
    curso = models.ForeignKey('cursos.Cursos', on_delete=models.CASCADE, verbose_name=_("Curso"))
    class_sis = models.CharField(max_length=20, choices=CLASS_CHOICES, default=NOME_IGUAL, verbose_name=_("Classificação Sistema"))
    class_prof = models.CharField(max_length=20, choices=CLASS_CHOICES, default=NOME_IGUAL, verbose_name=_("Classificação Professor"))
    obs_class_sis = models.CharField(max_length=100, verbose_name=_("Observações Sistema"))
    obs_class_prof = models.CharField(max_length=100, verbose_name=_("Observações Professor"))

def __str__(self):
        return self.nome_arquivo
