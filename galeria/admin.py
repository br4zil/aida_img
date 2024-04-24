# from django.contrib import admin
# from galeria.models import Fotografia
# from cursos.models import Cursos

# class ListandoFotografias(admin.ModelAdmin):
#     list_display = ("id", "nome", "legenda", "plublicada", "foto")
#     list_display_links = ("id", "nome")
#     search_fields = ("nome",)
#     list_editable = ("plublicada",)
#     list_per_page = 10
    
# class ListandoCursos(admin.ModelAdmin):
#     list_display = ("id", "nome", "instituicao", "professor", "data")
#     list_display_links = ("id", "nome")
#     search_fields = ("nome",)
#     list_per_page = 10

# admin.site.register(Fotografia, ListandoFotografias)
# admin.site.register(Cursos, ListandoCursos)