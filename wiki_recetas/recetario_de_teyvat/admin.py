from django.contrib import admin
from .models import Receta, Categoria, Comentario

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('Título', 'Región', 'Rareza', 'Autor', 'Fecha_de_creación')
    list_filter = ('Región', 'Rareza', 'Fecha_de_creación')
    search_fields = ('Título', 'Ingredientes', 'Autor__username')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('Nombre', 'Descripción')
    search_fields = ('Nombre',)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('Autor', 'Receta_asociada', 'Fecha_de_publicación')
    list_filter = ('Fecha_de_publicación',)
    search_fields = ('Contenido', 'Autor__username', 'Receta_asociada__Título')