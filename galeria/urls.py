from django.urls import path
from galeria.views import galeria, galeriaList

urlpatterns = [
    path('galeria', galeria, name='galeria'), 
    path('galeria-list/<int:id_curso>', galeriaList, name='galeria-list'),
]
