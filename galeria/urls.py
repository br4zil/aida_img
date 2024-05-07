from django.urls import path
from galeria.views import galeria, galeriaList, galeriaUpload, galeriaImagemDelete

urlpatterns = [
    path('galeria', galeria, name='galeria'), 
    path('galeria-upload', galeriaUpload, name='galeria-upload'), 
    path('galeria-imagem-delete/<int:id>', galeriaImagemDelete, name='galeria-imagem-delete'),
    path('galeria-list/<int:id_curso>', galeriaList, name='galeria-list'),
]
