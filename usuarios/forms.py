from django import forms

class LoginForms(forms.Form):
    usuario=forms.CharField(
        label="Usuário",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "autofocus": "autofocus"}
        )
    )
    senha=forms.CharField(
        label="Senha",  
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )