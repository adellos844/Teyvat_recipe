import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Receta, Comentario, Categoria
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

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    form.fields['username'].label = "Nombre de usuario"
    form.fields['password1'].label = "Contraseña"
    form.fields['password2'].label = "Confirmar contraseña"
    return render(request, 'registration/registro.html', {'form': form})

def buscar_recetas_externas(request):
    query = request.GET.get('q', '')
    resultados = []
    
    if query:
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"
        response = requests.get(url)
        data = response.json()
        
        if data and data['meals']:
            resultados = data['meals']
            
    return render(request, 'buscar_externo.html', {'resultados': resultados, 'query': query})

@login_required
def guardar_receta_externa(request):
    if request.method == 'POST':
        id_meal = request.POST.get('id_meal')
        
        url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={id_meal}"
        response = requests.get(url)
        data = response.json()
        
        if data and data['meals']:
            meal = data['meals'][0]
            
            categoria, _ = Categoria.objects.get_or_create(
                Nombre="Importada de API", 
                defaults={'Descripción': 'Recetas obtenidas de servicios externos.'}
            )
            
            ingredientes_lista = []
            for i in range(1, 21):
                ing = meal.get(f'strIngredient{i}')
                med = meal.get(f'strMeasure{i}')
                if ing and ing.strip():
                    ingredientes_lista.append(f"- {ing.strip()} ({med.strip() if med else ''})")
            
            ingredientes_texto = "\n".join(ingredientes_lista)
            
            nueva_receta = Receta.objects.create(
                Título=meal['strMeal'],
                Ingredientes=ingredientes_texto,
                Pasos_de_elaboración=meal['strInstructions'],
                Tiempo_de_preparación="30 minutos",  
                Región="Mondstadt",                  
                Autor=request.user,
                Rareza=3                             
            )
            url_imagen = meal.get('strMealThumb')
            if url_imagen:
                try:
                    img_response = requests.get(url_imagen)
                    if img_response.status_code == 200:
                        nombre_imagen = f"externa_{id_meal}.jpg"
                        nueva_receta.Imagen.save(nombre_imagen, ContentFile(img_response.content), save=False)
                except Exception:
                    pass

            nueva_receta.save()
            
    return redirect('lista_recetas')