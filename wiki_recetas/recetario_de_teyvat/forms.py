from django import forms
from .models import Receta, Comentario

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['Título', 'Ingredientes', 'Pasos_de_elaboración', 'Tiempo_de_preparación', 'Región', 'Rareza', 'Imagen']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['Contenido']