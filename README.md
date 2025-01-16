## 📚 **Proyecto Django: Gestor de Biblioteca**

### 📝 **Descripción del Proyecto**

Este proyecto es una aplicación de gestión de biblioteca construida con **Django**. Está diseñada para enseñar el uso del **Django Admin**, permitiendo administrar autores y libros de forma eficiente. Además, incluye una vista pública que muestra una lista de libros disponibles.

---

### 🚀 **Características Principales**

- **Gestión de Autores:** Crear, editar y eliminar autores desde el Django Admin.  
- **Gestión de Libros:** Administrar libros, asignar autores y cambiar su disponibilidad.  
- **Filtros y Búsqueda Avanzada:** Encontrar autores y libros fácilmente en el Admin.  
- **Acciones Personalizadas en Admin:** Marcar libros como no disponibles directamente desde el Admin.  
- **Vista Pública:** Mostrar una lista de libros disponibles en una página web.  

---

### 🛠️ **Tecnologías Usadas**

- **Python 3.x**
- **Django 5.x**
- **SQLite3** (base de datos por defecto)
- **HTML5** (para las plantillas públicas)
- **Chart.js** *(opcional, si deseas agregar gráficos interactivos)*

---

### 📂 **Estructura del Proyecto**

```plaintext
├── db.sqlite3
├── django_library
│   ├── settings.py   # Configuración principal de Django
│   ├── urls.py       # Rutas principales
│   ├── wsgi.py       # Interfaz WSGI para producción
│   ├── asgi.py       # Interfaz ASGI para aplicaciones asíncronas
├── library
│   ├── models.py     # Definición de modelos (Author, Book)
│   ├── admin.py      # Personalización del Admin de Django
│   ├── views.py      # Lógica de la vista pública
│   ├── urls.py       # Rutas de la app Library
│   ├── templates/
│   │   └── library/book_list.html  # Plantilla para la lista de libros
│   └── migrations/   # Archivos de migraciones
├── manage.py         # Herramienta de administración de Django
└── README.md         # Este archivo
```

---

### ⚙️ **Instalación y Configuración**

1. **Clonar el Repositorio:**
   ```bash
   git clone https://github.com/dibanez/django_library_workshop
   cd django_library_workshop
   ```

2. **Crear un Entorno Virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar Dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Realizar Migraciones:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crear un Superusuario para el Admin:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Iniciar el Servidor de Desarrollo:**
   ```bash
   python manage.py runserver
   ```

7. **Acceder a la Aplicación:**
   - **Admin Django:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
   - **Vista Pública:** [http://127.0.0.1:8000/books/](http://127.0.0.1:8000/books/)

---

### 🗂️ **Cargar Datos de Ejemplo (Opcional)**

1. Guarda el archivo `data.json` con datos de autores y libros.  
2. Ejecuta en el shell de Django:  
   ```bash
   python manage.py shell
   ```
3. Copia y pega el siguiente código en el shell:
   ```python
   import json
   from library.models import Author, Book

   with open('data.json', 'r') as file:
       data = json.load(file)

   author_mapping = {}
   for author_data in data['authors']:
       author, created = Author.objects.get_or_create(
           name=author_data['name'],
           defaults={
               'bio': author_data['bio'],
               'website': author_data['website']
           }
       )
       author_mapping[author_data['name']] = author

   for book_data in data['books']:
       Book.objects.get_or_create(
           title=book_data['title'],
           author=author_mapping[book_data['author']],
           published_date=book_data['published_date'],
           is_available=book_data['is_available']
       )

   print("✅ Datos importados correctamente.")
   ```

---

### 🌐 **Uso en el Admin de Django**

- **Agregar Autores:** Crea nuevos autores con nombre, biografía y enlace web.  
- **Agregar Libros:** Asocia libros a autores existentes y define su disponibilidad.  
- **Acciones Personalizadas:** Usa las acciones en el Admin para marcar libros como no disponibles.

---

### 🧪 **Tests**

El proyecto incluye una suite completa de tests que cubren modelos, admin y vistas:

1. **Ejecutar todos los tests:**
   ```bash
   python manage.py test

---

### 🤝 **Contribuciones**

¡Toda contribución es bienvenida! Si deseas mejorar el proyecto, por favor abre un **Pull Request** o un **Issue** en GitHub.

---

### 🛡️ **Licencia**

Este proyecto está bajo la **MIT License**.

---

