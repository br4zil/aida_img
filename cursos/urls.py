from django.urls import path
from cursos.views import cursos, cursosUpdate, cursosCreate, cursosDelete
urlpatterns = [
    path('cursos', cursos, name='cursos'), 
    path('cursos-update/<int:id>', cursosUpdate, name='cursos-update'),
    path('cursos-create', cursosCreate, name='cursos-create'),
    path('cursos-delete/<int:id>', cursosDelete, name='cursos-delete'),
]
