# Teyvat_recipe

Aplicación web de recetario inspirada en Teyvat y Genshin Impact, desarrollada con Django para la gestión de recetas, comentarios y búsquedas externas.

## Enlace al código fuente

- Repositorio: `https://github.com/adellos844/Teyvat_recipe`  

## Manual básico de instalación y ejecución

### Requisitos

- Python 3.10 o superior
- pip
- Git

### Dependencias principales

- Django 6.0.5
- requests
- Pillow

### Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/adellos844/Teyvat_recipe.git
cd Teyvat_recipe/wiki_recetas
```

2. Crear un entorno virtual:

```bash
python -m venv venv
```

3. Activar el entorno virtual:

```powershell
venv\Scripts\Activate.ps1
```

4. Instalar dependencias:

```bash
pip install django==6.0.5 requests pillow
```

5. Crear la base de datos y ejecutar migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Crear un superusuario:

```bash
python manage.py createsuperuser
```

7. Ejecutar el servidor:

```bash
python manage.py runserver
```

8. Abrir en el navegador:

- http://127.0.0.1:8000/

### Notas de configuración

- El proyecto utiliza SQLite como base de datos local (`db.sqlite3`).
- Los archivos estáticos se cargan desde `wiki_recetas/static/`.
- Las imágenes subidas se almacenan en `wiki_recetas/media/`.

## Tecnologías utilizadas

- Django 6.0.5
- Python 3.10+  
- SQLite3
- HTML y CSS
- Django ORM
- Django templates
- Librería `requests` para consumo de API externa
- Librería `Pillow` para soporte de campos de imagen en Django

### Uso de IA generativa

- Se ha utilizado asistencia de IA generativa para resolver problemas de código, depuración y organización de plantillas.
- Herramienta utilizada: GitHub Copilot 
- Finalidad: ayuda en la corrección de errores de plantillas, configuración de rutas y explicación de la arquitectura.

## Diseño y arquitectura

### Organización de carpetas

- `wiki_recetas/`
  - `manage.py` -> comando de administración de Django
  - `db.sqlite3` -> base de datos SQLite local
  - `teyvat_recipe/` -> proyecto Django principal
    - `settings.py` -> configuración general del proyecto
    - `urls.py` -> rutas principales del proyecto
    - `wsgi.py`, `asgi.py` -> despliegue
  - `recetario_de_teyvat/` -> aplicación principal
    - `models.py` -> modelos de datos
    - `views.py` -> lógica de presentación
    - `forms.py` -> formularios de Django
    - `templates/` -> plantillas HTML
    - `static/` -> estilos CSS y recursos estáticos
    - `migrations/` -> control de cambios en el modelo

### Rutas principales

- `/` -> listado de recetas (`lista_recetas`)
- `/recetas/<int:pk>/` -> detalle de receta (`detalle_recetas`)
- `/recetas/crear/` -> crear receta nueva (`crear_receta`)
- `/recetas/<int:pk>/editar/` -> editar receta (`editar_receta`)
- `/recetas/<int:pk>/eliminar/` -> eliminar receta (`eliminar_receta`)
- `/comentarios/<int:pk>/eliminar/` -> eliminar comentario (`eliminar_comentario`)
- `/login/` -> inicio de sesión
- `/logout/` -> cerrar sesión
- `/registro/` -> registro de usuario
- `/buscar-externo/` -> búsqueda de recetas externas
- `/guardar-externo/` -> guardar recetas desde API externa

### Modelos y estructura de base de datos

- `Receta`
  - `Título` (CharField)
  - `Ingredientes` (TextField)
  - `Pasos_de_elaboración` (TextField)
  - `Tiempo_de_preparación` (CharField)
  - `Región` (CharField con opciones)
  - `Autor` (ForeignKey a `User`)
  - `Rareza` (PositiveIntegerField)
  - `Fecha_de_creación` (DateTimeField)
  - `Imagen` (ImageField)

- `Comentario`
  - `Receta_asociada` (ForeignKey a `Receta`)
  - `Autor` (ForeignKey a `User`)
  - `Contenido` (TextField)
  - `Fecha_de_publicación` (DateTimeField)

- `Categoria`
  - `Nombre` (CharField)
  - `Descripción` (TextField)

### Vistas principales

- `lista_recetas` -> muestra todas las recetas, con filtro por búsqueda y por región.
- `detalle_receta` -> muestra receta detallada, formulario de comentarios y gestión de acciones de autor.
- `crear_receta` / `editar_receta` -> formularios para crear o editar recetas.
- `eliminar_receta` / `eliminar_comentario` -> confirmación y borrado seguro.
- `registro` -> creación de usuario con formulario integrado.
- `buscar_recetas_externas` -> consulta a la API pública `TheMealDB`.
- `guardar_receta_externa` -> guarda una receta importada desde la API en la base local.

## Funcionalidades implementadas

- Listado de recetas ordenado por fecha de creación.
- Filtrado de recetas por texto y región.
- Gestión de usuarios: registro, login, logout.
- Creación, edición y eliminación de recetas (con permisos del autor).
- Comentarios por usuario autenticado en cada receta.
- Carga y visualización de imagen de receta.
- Búsqueda de recetas externas en `TheMealDB` y guardado en la aplicación.
- Uso de plantilla base común para estilos compartidos.
- Soporte de archivos estáticos y media local.

## Conclusiones y mejoras

### Conclusiones

La aplicación funciona como un recetario básico con autenticación, CRUD de recetas y comentarios, además de integración con una API externa. El uso de plantillas heredadas permite mantener un diseño consistente y simplifica actualizaciones de estilo.

### Mejoras futuras

- Mejorar la interfaz con un diseño responsive completo.
- Guardar en caché los resultados de la API externa para reducir llamadas.
- Desplegar en un servidor real y usar una base de datos PostgreSQL.
