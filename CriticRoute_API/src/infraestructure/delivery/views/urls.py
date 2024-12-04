from django.urls import path

from CriticRoute_API.src.infraestructure.config.views_factory import get_buscar_proyectos_factory, \
    get_buscar_proyecto_id_factory, post_nuevo_proyecto_factory

# Define el prefijo para las rutas relacionadas con los proyectos
proyecto_path = 'proyecto'

# Define las rutas específicas de la aplicación relacionadas con los proyectos
urlpatterns = [
    # Ruta para crear un nuevo proyecto mediante el uso de la función `post_nuevo_proyecto_factory`
    path(f'{proyecto_path}', post_nuevo_proyecto_factory, name='nuevo_proyecto'),

    # Ruta para buscar todos los proyectos asociados al usuario, utilizando la función `get_buscar_proyectos_factory`
    path(f'{proyecto_path}/', get_buscar_proyectos_factory, name='buscar_proyectos'),

    # Ruta para obtener los detalles de un proyecto específico por su ID, utilizando la función
    # `get_buscar_proyecto_id_factory`
    path(f'{proyecto_path}/<int:id_proyecto>', get_buscar_proyecto_id_factory, name='buscar_proyecto_id')
]
