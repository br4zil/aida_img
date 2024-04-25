from django import forms
from .models import ImagensCurso

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ImagensCursoForm(forms.ModelForm):
    class Meta:
        model = ImagensCurso
        fields = ['nome_arquivo', 'imagem', 'class_sis', 'class_prof', 'obs_class_sis', 'obs_class_prof']
    
    # Use forms.FileInput em vez de ClearableFileInput para suportar múltiplos arquivos
    imagem = MultipleFileField()

