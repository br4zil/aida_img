from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Cursos(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False, verbose_name=_("Nome do Curso"))
    instituicao = models.TextField(max_length=100, null=True, blank=True, verbose_name=_("Instituição"))
    professor = models.TextField(max_length=100, null=True, blank=True, verbose_name=_("Professor"))
    data = models.DateTimeField(default=datetime.now, blank=False, verbose_name=_("Data"))
    imagens_esperadas = models.TextField(null=True, blank=True, verbose_name=_("Descrições do que é esperado nas imagens (Virgula para separar)"))
    usuario = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="user"
    )
    
    def __str__(self):
        return self.nome
