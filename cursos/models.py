from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Cursos(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    instituicao = models.TextField(max_length=100, null=False, blank=False)
    professor = models.TextField(max_length=100, null=False, blank=False)
    data = models.DateTimeField(default=datetime.now, blank=False)
    usuario = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="user"
    )
    
    def __str__(self):
        return self.nome
