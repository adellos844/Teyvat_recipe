from django.shortcuts import render, get_object_or_404
from .models import Receta

def lista_recetas(request):
    recetas = Receta.objects.all().order_by('-Fecha_de_creación')
    return render(request, 'recetario/lista_recetas.html', {'recetas': recetas})

def detalle_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    comentarios = receta.comentario_set.all().order_by('-Fecha_de_publicación')
    
    contexto = {
        'receta': receta,
        'comentarios': comentarios
    }
    return render(request, 'recetario/detalle_receta.html', contexto)