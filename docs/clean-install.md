# Step-by-Step Guide (Django Classic)

> [!NOTE]
> **Prerequisite:** It is assumed that Python is already installed.

## Step 1: Environment Setup

Always use a virtual environment to prevent project dependencies from conflicting with your system.

1. Create a project folder

```Bash copy
mkdir my_landing
```

```Bash copy
cd my_landing
```

2. Create a virtual environment

```Bash copy
python -m venv venv
```

3. Activate it (Windows)

```Bash copy
venv\Scripts\activate
```

4. Activate it (Mac/Linux)

```Bash copy
source venv/bin/activate
```

5. Install Django

```Bash copy
pip install django
```

## Step 2: Creating the Project and Application

In Django, a project represents the global configuration, while an application handles specific functionality.

1. Create a project (the dot at the end is important to avoid unnecessary nesting)

```Bash copy
django-admin startproject config .
```

2. Create a landing page application (let's call it `'pages'` or `'main'`)

```Bash copy
python manage.py startapp core
```

Now, you need to register the `core` app in the settings. Open `config/settings.py` and locate `INSTALLED_APPS`:

```Python copy
INSTALLED_APPS = [
    # ... standard Django applications
    'core',  # Add our application
]
```

In this file, find the section `TEMPLATES`:

1. `'DIRS': [BASE_DIR / 'templates']`

This line defines where Django looks for your HTML files.

* `BASE_DIR`: This is the path to your project's root directory (the one containing `manage.py`).

* `/ 'templates'`: This tells Django: "Look for global templates in a folder named `templates` located in the project root."

**Why is this important?**

If you create a `index.html` file in the root templates folder, Django will only find it because of this setting. If you leave the `DIRS` list empty, Django will only look for templates inside specific app folders (provided that `APP_DIRS: True` is enabled).

2. `'django.template.context_processors.request'`

This is a "magic" setting that makes the request object (the user's request) available inside any HTML template without needing to pass it manually from `views.py`.

**What does this mean in practice?**

Thanks to this line, you can use the following in your templates:

* `{{ request.user }}` — to display the name of the logged-in user.

* `{% if request.path == '/about/' %}` — to highlight an active menu link (exactly what we discussed earlier).

* `{{ request.GET.page }}` — to retrieve parameters directly from the URL.

```Python copy
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],
        ...
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                ...
            ],
        },
    },
]
]
```

In this file, find the section `STATIC_URL` and `STATICFILES_DIRS`:

1. `STATIC_URL = 'static/'`

This is the public URL.

It tells Django which prefix to add to the URL so the browser understands: "Aha, this is a request for an image or a stylesheet, not an HTML page."

* The `{% load static %}` tag is Django's standard way to include static content (CSS, JS, Images). Add to the top of the HTML file.

* **How it works:** When you write `{% static 'css/style.css' %}` in a template, Django converts it into `/static/css/style.css`.

> [!IMPORTANT]
> This setting doesn't tell Django where the files are located on your hard drive. It only defines what the link will look like in the browser.

2. `STATICFILES_DIRS`

This is **a list of file paths on your computer** where Django should look for static files during development.

* `BASE_DIR`: This is the path to your project's root directory (where `manage.py` is located).

* **What this means**: You’re telling Django: "If someone requests a `static` file, go check the static folder located right in my project's root."

```Python copy
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

In this file, find the section `MEDIA_URL` and `MEDIA_ROOT`

1. `MEDIA_URL = '/media/'`

This is the **public URL** where your files will be accessible in the browser.

* When you write `{{ item.image.url }}` in a template, Django will prepend this exact string to the file path.

* For example, if you upload `logo.png`, its URL on the site will be: `http://127.0.0.1:8000/media/logo.png`.

2. `MEDIA_ROOT = BASE_DIR / 'media'`

This is **the absolute path on your system** (hard drive) where Django will physically store the uploaded files.

* `BASE_DIR` represents the path to your project folder.

* If your project folder is `C:\MyProject`, then the files will be saved in `C:\MyProject\media`.

```Python copy
MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'
```

## Step 3: Database Design (Models)

To make landing page text and images editable via the admin panel, we need to create models. Open `core/models.py`.

**Example** models for the _"Benefits"_ block and _"Site Settings"_:

```Python copy
from django.db import models

# Model for general settings (header, logo, contacts)
class SiteSettings(models.Model):
    title = models.CharField("Site Title", max_length=200)
    logo = models.ImageField("Logo", upload_to='images/')
    contact_email = models.EmailField("Contact Email")
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

# Model for the "Services" or "Benefits" section
class Service(models.Model):
    title = models.CharField("Service Name", max_length=100)
    description = models.TextField("Description")
    icon = models.ImageField("Icon", upload_to='services/', blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Service"
```

_Note:_ To work with images, you will need the Pillow library:

```Bash copy
pip install Pillow
```

## Step 4: Applying Migrations

Inform the database about our new models.

```Bash copy
python manage.py makemigrations
```

```Bash copy
python manage.py migrate
```

## Step 5: Admin Panel Configuration

To manage the models, you must register them. Open `core/admin.py`:

```Python copy
from django.contrib import admin
from .models import SiteSettings, Service

# Simple registration
admin.site.register(Service)

# Registration with restrictions (to ensure a single site configuration)
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    # Disable adding new entries if there's already one (optional, logic implemented separately)
    pass
```

Now, create a superuser to log in:

* Follow the instructions (enter your username and password)
```Bash copy
python manage.py createsuperuser
```

## Step 6: Display Logic (Views)

We need to fetch the data from the database and pass it to the HTML template. Open `core/views.py`:

```Python copy
from django.shortcuts import render
from .models import SiteSettings, Service

def index(request):
    # Get the first settings record (or None if empty)
    settings = SiteSettings.objects.first()
    # Get all services
    services = Service.objects.all()
    
    context = {
        'settings': settings,
        'services': services,
    }
    return render(request, 'index.html', context)
```

## Step 7: Routing (URLs)

Link the website URL to our view function.

1. Create the file `core/urls.py`:

```Python copy
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
]
```

2. Include it in the main `config/urls.py`:

```Python copy
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# Setting up media file distribution (images) in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Don't forget to add Media settings to the bottom of `config/settings.py`:

```Python copy
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## Step 8: Template (HTML)

Create a `templates` folder in the root directory (or inside the `core` app).
If created in the root, add the path to `settings.py` under `TEMPLATES -> 'DIRS': [BASE_DIR / 'templates']`.

File: `templates/index.html`:

```HTML copy
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{{ settings.title|default:"Мой Лендинг" }}</title>
    </head>
<body>

    <header>
        {% if settings.logo %}
            <img src="{{ settings.logo.url }}" alt="Logo" width="100">
        {% endif %}
        <h1>{{ settings.title }}</h1>
    </header>

    <section id="services">
        <h2>Наши услуги</h2>
        <div class="services-list">
            {% for service in services %}
                <div class="service-card">
                    {% if service.icon %}
                        <img src="{{ service.icon.url }}" alt="{{ service.title }}">
                    {% endif %}
                    <h3>{{ service.title }}</h3>
                    <p>{{ service.description }}</p>
                </div>
            {% endfor %}
        </div>
    </section>

    <footer>
        Контакты: {{ settings.contact_email }}
    </footer>

</body>
</html>
```

## Summary

Now, run the server:

```Bash copy
python manage.py runserver
```

1. Go to `http://127.0.0.1:8000/admin/` — add your site settings and a few services.

2. Go to `http://127.0.0.1:8000/` — you will see your landing page populated with data from the admin panel.