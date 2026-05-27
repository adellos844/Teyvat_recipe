from django.db import models
from django.contrib.auth.models import User  

class Receta(models.Model):
    REGIONES_TEYVAT = [
        ('mondstadt', 'Mondstadt'),
        ('liyue', 'Liyue'),
        ('inazuma', 'Inazuma'),
        ('sumeru', 'Sumeru'),
        ('fontaine', 'Fontaine'),
        ('natlan', 'Natlan'),
        ('snezhnaya', 'Snezhnaya'),
    ]
    Título = models.CharField(max_length=200)
    Ingredientes = models.TextField()
    Pasos_de_elaboración = models.TextField()
    Tiempo_de_preparación = models.CharField(max_length=50)
    Región = models.CharField(max_length=100, choices=REGIONES_TEYVAT)
    Autor = models.ForeignKey(User, on_delete=models.CASCADE)  
    Rareza = models.PositiveIntegerField(help_text="Estrellas del 1 al 5")
    Fecha_de_creación = models.DateTimeField(auto_now_add=True)
    Imagen_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.Título
    
class Categoria(models.Model):
    Nombre = models.CharField(max_length=100)
    Descripción = models.TextField()

    def __str__(self):
        return self.Nombre

class Comentario(models.Model):
    Receta_asociada = models.ForeignKey(Receta, on_delete=models.CASCADE)
    Autor = models.ForeignKey(User, on_delete=models.CASCADE)
    Contenido = models.TextField()
    Fecha_de_publicación = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.Autor.username} en {self.Receta_asociada.Título}'