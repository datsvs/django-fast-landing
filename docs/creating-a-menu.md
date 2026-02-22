# Creating a Menu

## Step 1: Installation and configuration django-admin-sortable2

* Installation

```Bash copy
pip install django-admin-sortable2
```

* Registration

Add it to `INSTALLED_APPS` in your `settings.py` file:

```Python copy
INSTALLED_APPS = [
    ...
    'adminsortable2',
    ...
]
```

## Step 3: Setting up the admin panel (admin.py)

```Python copy
from django.contrib import admin
# Special mixin for inlines
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from .models import Menu, MenuItem

# 1. Describe how the items will appear inside the menu
class MenuItemInline(SortableInlineAdminMixin, admin.TabularInline):
    model = MenuItem
    # How many empty lines for new items to display at once
    extra = 1

# 2. Register the main menu model
@admin.register(Menu)
class MenuAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['name', 'slug']
    # Add items to the menu editing page
    inlines = [MenuItemInline]
```

## Step 4: Setting up the Model (models.py)

```Python copy
from django.db import models

# In the admin panel, there is a Menu object, at the bottom you will see a table with all its MenuItems.
class Menu(models.Model):
    name = models.CharField("Menu Title", max_length=100)
    slug = models.SlugField("Slug", unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Site Menu"
        verbose_name_plural = "Site Menu"

# Creating a menu in the admin panel
class MenuItem(models.Model):
    # Add a ForeignKey relationship
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    title = models.CharField("Name", max_length=100)
    url = models.CharField("Link", max_length=200, help_text="For example: #about или https://google.com")
    order = models.PositiveIntegerField("Order", default=0)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order', 'title']
```

## Step 5: Setting up the Settings (settings.py)

* Make sure the request processor is enabled in the `TEMPLATES` section (it's enabled by default in new Django projects). This gives the template access to the `request` object.

* Make sure Django knows where to find your templates. In `settings.py`, the `TEMPLATES` section should look something like this:

```Python copy
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],
        ...
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                ....
            ],
        },
    },
]
```

## Step 6: Display your custom menu anywhere on the site with one short command

1. **Create the folder structure**

Inside your app (let’s assume it’s called core), create a directory named `templatetags`. It must contain an empty `__init__.py` file.

```Bash copy
core/
    templates/
        menu/
            menu-default.html
            menu-header.html
            menu-loader.html
	    index.html
    models.py
    templatetags/
        __init__.py
        menu_tags.py
```

2. **Write the tag logic (`menu_tags.py`)**

In this file, define how Django should fetch the menu items from the database.

```Python copy
from django import template
# Предположим, у вас есть модель меню
from core.models import MenuItem

register = template.Library()

@register.inclusion_tag('menu/menu-loader.html', takes_context=True)
def show_menu(context, slug, template_name='menu-default'):
    # Получаем пункты меню из базы
    items = MenuItem.objects.filter(menu__slug=slug).order_by('order')
    # Формируем путь к конкретному файлу верстки
    full_template_path = f'menu/{template_name}.html'
    return {
        'menu_items': items,
        'template_name': full_template_path,
        # Чтобы работали активные ссылки
        'request': context.get('request'),
    }
```

3. **Create the menu template (`core/templates/menu/menu-header.html`)**

This file will contain only the HTML code for the menu list itself. Create it in the `core/templates/menu/` directory.

```HTML copy
{% for item in menu_items %}
    <li class="group relative">
        <a
        href="{{ item.url }}"
        class="ic-page-scroll mx-8 flex py-2 text-base font-medium text-body-light-12 group-hover:text-primary dark:text-body-dark-12 {% if forloop.first %}lg:mx-0{% else %}lg:mr-0{% endif %} lg:inline-flex lg:px-0 lg:py-6 lg:text-primary-color lg:dark:text-primary-color lg:group-hover:text-primary-color lg:group-hover:opacity-70 
        {% if request.path == item.url %}active{% endif %}"
        role="menuitem"
        > {{ item.title }}
        </a>
    </li>
{% endfor %}
```

4. **Create a default menu template (`core/templates/menu/menu-default.html`)**

This file will contain plain HTML without CSS styles. It serves as a fallback if no specific template is defined. Create it in `core/templates/menu/`

```HTML copy
{% for item in menu_items %}
    <li>
        <a
        href="{{ item.url }}"
        > {{ item.title }}
        </a>
    </li>
{% endfor %}
```

5. **Create the `menu-loader.html` wrapper**

This file acts as a dispatcher. It will dynamically include the template you specify.

```Bash copy
{% include template_name %}
```
6. **Use it anywhere!**

Now, in your main template (e.g., `index.html`), you need to do two things:

* Load the tag library at the very top.

```Bash copy
{% load menu_tags %}
```

* Call the command.

```Bash copy
{% show_menu 'menu-header' 'menu-header' %}
```

7. **Highlighting the "Active" menu item**

To help users understand which page they are currently on, add a simple check to the `menu-header.html` template.

```HTML copy
...
    <a
    ...
    class="...
    {% if request.path == item.url %}active{% endif %}"
    ...
    </a>
...
```

> [!IMPORTANT]
> For `request.path` to work inside the tag, ensure that `'django.template.context_processors.request'` is included in the `TEMPLATES` section of your `settings.py`.