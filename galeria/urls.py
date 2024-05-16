from django.urls import path
from galeria.views import galeria, galeriaList, galeriaUpload, galeriaImagemDelete, galeriaImagemDeleteAll, galeriaIdentificarIDA, galeriaIdentificarIDANoWS
from . import consumers

urlpatterns = [
    path('galeria', galeria, name='galeria'), 
    path('galeria-upload', galeriaUpload, name='galeria-upload'), 
    path('galeria-imagem-delete/<int:id>', galeriaImagemDelete, name='galeria-imagem-delete'),
    path('galeria-imagem-delete', galeriaImagemDeleteAll, name='galeria-imagem-delete-all'),
    path('galeria-list/<int:id_curso>', galeriaList, name='galeria-list'),
    path('galeria-identificarIDA', galeriaIdentificarIDA, name='galeria-identificarIDA'),
    path('galeria-identificarIDANoWS', galeriaIdentificarIDANoWS, name='galeria-identificarIDANoWS'),
]
