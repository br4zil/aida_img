from django.db import models
from django.utils.translation import gettext_lazy as _
import os
from django.conf import settings
from django.core.files.storage import default_storage

def upload_to(instance, filename):
    # Cria o caminho de destino com base no ID do usuário e do curso
    user_id = str(instance.curso.usuario.id)
    curso_id = str(instance.curso.id)
    
    # Cria um novo nome de arquivo ou usa o existente
    file_extension = os.path.splitext(filename)[-1]
    novo_id = ImagensCurso.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0
    novo_id += 1
    novo_nome_arquivo = f'{novo_id}{file_extension}'
    
    if 'aidaimg.com' in instance.obs_class_sis:
        # Caminho completo de destino com base em MEDIA_ROOT
        caminho_destino = os.path.join('images', 'imagens_cursos', user_id, curso_id, novo_nome_arquivo)
    else:
        caminho_destino = os.path.join('images', 'imagens_cursosLocal', user_id, curso_id, novo_nome_arquivo)
    instance.obs_class_sis = ''
    
    return caminho_destino


class ImagensCurso(models.Model):
    # Escolhas de classes
    NOME_IGUAL = 'IDA_igual'
    NOME_MONO = 'IDA_mono'
    NOME_COPIA = 'IDA_copia'
    NOME_COPIA_WEB = 'IDA_copia_web'
    NOME_CLASS = 'IDA_class'
    NOME_NORMAL = 'Normal'

    CLASS_CHOICES = [
        (NOME_IGUAL, _('IDA Igual')),
        (NOME_MONO, _('IDA Mono')),
        (NOME_COPIA, _('IDA Cópia')),
        (NOME_COPIA_WEB, _('IDA Cópia Web')),
        (NOME_CLASS, _('IDA Class')),
        (NOME_NORMAL, _('Normal')),
    ]

    nome_arquivo = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Nome do Arquivo"))
    imagem = models.ImageField(upload_to=upload_to, null=True, blank=True, verbose_name=_("Imagem"))
    curso = models.ForeignKey('cursos.Cursos', null=True, blank=True, on_delete=models.CASCADE, verbose_name=_("Curso"))
    class_sis = models.CharField(max_length=20, null=True, blank=True, choices=CLASS_CHOICES, default=None, verbose_name=_("Classificação Sistema"))
    class_prof = models.CharField(max_length=20, null=True, blank=True, choices=CLASS_CHOICES, default=None, verbose_name=_("Classificação Professor"))
    obs_class_sis = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Observações Sistema"))
    obs_class_prof = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Observações Professor"))

    def __str__(self):
        return self.nome_arquivo

    def save(self, *args, **kwargs):
        # Verifica se a instância é nova (nunca foi salva antes)
        is_new_instance = self.pk is None

        # Se a instância é nova e há uma imagem associada
        if is_new_instance and self.imagem:
            # Salve o nome original do arquivo sem o caminho no campo nome_arquivo
            self.nome_arquivo = os.path.basename(self.imagem.name)

        # Chama o método save da classe pai (models.Model) para salvar a instância
        super().save(*args, **kwargs)
        