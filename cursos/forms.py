from django.forms import ModelForm, forms, Textarea, TextInput, HiddenInput, DateField, DateInput
from datetime import datetime
from .models import Cursos

class CursosForm(ModelForm):
    class Meta:
        model = Cursos
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        # Chama o método __init__() da classe base
        super().__init__(*args, **kwargs)
        
        # Definir a data atual para um campo específico (por exemplo, 'data')
        self.fields['data'].initial = datetime.now().date()
        
        for field_name, field in self.fields.items():
            # Verifique se o campo é um Textarea
            if isinstance(field.widget, Textarea):
                # Substitui o widget Textarea por TextInput
                field.widget = TextInput(attrs={'class': 'form-control'})
            else:
                # Adiciona a classe 'form-control' a outros campos
                field.widget.attrs.update({'class': 'form-control'})
            # Verifica se o nome do campo é 'usuario'
            if field_name == 'usuario' or field_name == 'data':
                # Torna o campo invisível
                field.widget = HiddenInput()  
            
   
                

            # Verifica se o campo é um campo de data
            # if field_name == 'data':
            #if isinstance(field.widget, DateInput):
                # Adiciona a classe 'datepicker' para ativar a funcionalidade de calendário
                # field.widget.attrs.update({
                #     'class': 'form-control datepicker',
                #     'placeholder': 'Selecione uma data',
                #     'type': 'date'
                # })

                  
            # Verifica se o campo é um campo de data
            #if isinstance(field, DateTimeField):
            # if field_name == 'data':
            #     # Adiciona uma classe ao widget para usar um calendário de uma biblioteca externa
            #     field.widget = DateField(
            #         label="Data",
            #         required=True,
            #         widget=DateInput(format="%d-%m-%Y", attrs={"type": "date"}),
            #         input_formats=["%d-%m-%Y"]
            #     )                           