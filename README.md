# Guía de Instalación y Ejecución del Proyecto

Este documento proporciona las instrucciones necesarias para clonar, instalar dependencias y ejecutar el proyecto de manera local. También incluye instrucciones para ejecutar el proyecto utilizando Docker.

## Requisitos previos

Antes de empezar, asegúrate de tener los siguientes programas instalados en tu máquina:

- **[Python 3.10+](https://www.python.org/downloads/)**: Necesario para ejecutar el proyecto en un entorno local.
- **[Docker](https://www.docker.com/get-started)**: Recomendado si prefieres ejecutar el proyecto dentro de un contenedor Docker.
- **[Git](https://git-scm.com/downloads)**: Necesario para clonar el repositorio.

## Pasos para ejecutar el proyecto

### 1. Clonar el repositorio

Clona el repositorio en tu máquina local utilizando Git:

```bash
git clone https://github.com/danielmatt-dev/CriticRoute_API.git
cd CriticRoute_API
```

### 2. Crear un entorno virtual (opcional pero recomendado)

Es recomendable crear un entorno virtual para manejar las dependencias del proyecto sin interferir con otros proyectos de Python. Ejecuta el siguiente comando para crear el entorno:

#### En Linux/macOS:
```bash
python -m venv .venv
source .venv/bin/activate
```

#### En Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar las dependencias

Instala todas las dependencias necesarias para el proyecto utilizando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Crea un archivo `.env` en la raíz del proyecto y agrega las siguientes variables de entorno para la configuración de Django y la base de datos:

```bash
DJANGO_SECRET_KEY=tu-secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DATABASE=tu_base_de_datos
POSTGRES_USER=tu_usuario
POSTGRES_PASSWORD=tu_contraseña
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 5. Ejecutar las migraciones de la base de datos

Si es la primera vez que ejecutas el proyecto, realiza las migraciones para crear las tablas necesarias en la base de datos:

```bash
python manage.py migrate
```

### 6. Ejecutar el servidor de desarrollo

Una vez configurado el entorno y las dependencias, ejecuta el servidor local de Django:

```bash
python manage.py runserver
```

Accede a la API en [http://localhost:8000/](http://localhost:8000/).

## Uso con Docker (Opcional)

Si prefieres ejecutar el proyecto en un contenedor Docker, sigue estos pasos:

### 1. Clonar la imagen desde Docker Hub

Puedes clonar la imagen preconfigurada desde Docker Hub usando el siguiente comando. Asegúrate de usar el **tag** correspondiente a la versión que desees ejecutar (por ejemplo, `v1.0.1`):

```bash
docker pull danielmatt/criticroute_api:<tag>
```

Reemplaza `<tag>` con la versión del tag que desees usar (por ejemplo, `v1.0.1`). Esta imagen contiene todo lo necesario para ejecutar el proyecto en un contenedor Docker.

### 2. Ejecutar el contenedor Docker

Luego, ejecuta el contenedor Docker y mapea el puerto 8000:

```bash
docker run --env-file .env -p 8000:8000 danielmatt/criticroute_api:<tag>
```

El archivo `.env` debe estar en la raíz del proyecto para que las variables de entorno se carguen correctamente dentro del contenedor.

Accede a la API en [http://localhost:8000/](http://localhost:8000/) como lo harías con el servidor local de Django.

### Explicación:
- **`<tag>`**: Este es el marcador de posición que debes reemplazar con el tag específico de la imagen de Docker que deseas usar, por ejemplo, `v1.0.1` o cualquier versión que hayas etiquetado previamente en tu repositorio de Docker Hub.
