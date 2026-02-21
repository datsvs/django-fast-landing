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