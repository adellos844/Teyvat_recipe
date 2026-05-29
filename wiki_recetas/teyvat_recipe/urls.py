"""
URL configuration for teyvat_recipe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from recetario_de_teyvat import views as recetario_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', recetario_views.lista_recetas, name='lista_recetas'),
    path('recetas/<int:pk>/', recetario_views.detalle_receta, name='detalle_recetas'),
    path('recetas/crear/', recetario_views.crear_receta, name='crear_receta'),
    path('recetas/<int:pk>/editar/', recetario_views.editar_receta, name='editar_receta'),
    path('recetas/<int:pk>/eliminar/', recetario_views.eliminar_receta, name='eliminar_receta'),
    path('comentarios/<int:pk>/eliminar/', recetario_views.eliminar_comentario, name='eliminar_comentario'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', recetario_views.registro, name='registro'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)