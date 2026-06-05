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
    Imagen = models.ImageField(upload_to='recetas/', null=True, blank=True)

    @property
    def puntuacion_media(self):
        puntuaciones = self.puntuacion_set.all()
        if not puntuaciones:
            return 0
        return round(sum(p.Valor for p in puntuaciones) / puntuaciones.count(), 1)

    @property
    def numero_puntuaciones(self):
        return self.puntuacion_set.count()

    def puntuacion_usuario(self, usuario):
        if not usuario.is_authenticated:
            return None
        return self.puntuacion_set.filter(Autor=usuario).first()

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

class Puntuacion(models.Model):
    Receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    Autor = models.ForeignKey(User, on_delete=models.CASCADE)
    Valor = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    Fecha = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('Receta', 'Autor')

    def __str__(self):
        return f'Puntuación {self.Valor} de {self.Autor.username} en {self.Receta.Título}'