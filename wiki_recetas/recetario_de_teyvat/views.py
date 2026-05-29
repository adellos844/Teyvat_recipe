from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Receta, Comentario
from .forms import RecetaForm, ComentarioForm

def lista_recetas(request):
    recetas = Receta.objects.all().order_by('-Fecha_de_creación')
    
    buscar = request.GET.get('q')
    if buscar:
        recetas = recetas.filter(Título__icontains=buscar) | recetas.filter(Ingredientes__icontains=buscar)
        
    region = request.GET.get('region')
    if region:
        recetas = recetas.filter(Región=region)
        
    autor_id = request.GET.get('autor')
    if autor_id:
        recetas = recetas.filter(Autor_id=autor_id)

    return render(request, 'recetario/lista_recetas.html', {'recetas': recetas})

def detalle_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    comentarios = receta.comentario_set.all().order_by('Fecha_de_publicación')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login') 
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.Receta_asociada = receta
            comentario.Autor = request.user
            comentario.save()
            return redirect('detalle_recetas', pk=receta.pk)
    else:
        form = ComentarioForm()

    return render(request, 'recetario/detalle_recetas.html', {
        'receta': receta, 
        'comentarios': comentarios,
        'form': form
    })

@login_required
def crear_receta(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES) 
        if form.is_valid():
            receta = form.save(commit=False)
            receta.Autor = request.user
            receta.save()
            return redirect('lista_recetas')
    else:
        form = RecetaForm()
    return render(request, 'recetario/formulario_receta.html', {'form': form, 'accion': 'Crear'})

@login_required
def editar_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    if receta.Autor != request.user:
        raise PermissionDenied 
        
    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES, instance=receta)
        if form.is_valid():
            form.save()
            return redirect('detalle_receta', pk=receta.pk)
    else:
        form = RecetaForm(instance=receta)
    return render(request, 'recetario/formulario_receta.html', {'form': form, 'accion': 'Editar'})

@login_required
def eliminar_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    if receta.Autor != request.user:
        raise PermissionDenied
        
    if request.method == 'POST':
        receta.delete()
        return redirect('lista_recetas')
    return render(request, 'recetario/confirmar_eliminar.html', {'objeto': receta.Título, 'tipo': 'receta'})

@login_required
def eliminar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    if comentario.Autor != request.user:
        raise PermissionDenied
        
    receta_pk = comentario.Receta_asociada.pk
    if request.method == 'POST':
        comentario.delete()
        return redirect('detalle_recetas', pk=receta_pk)
    return render(request, 'recetario/confirmar_eliminar.html', {'objeto': comentario.Contenido[:30], 'tipo': 'comentario'})