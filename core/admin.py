from django.contrib import admin
# Специальный миксин для инлайнов
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from .models import Menu, MenuItem, SiteSettings, Service

# 1. Описываем, как пункты будут выглядеть внутри меню
class MenuItemInline(SortableInlineAdminMixin, admin.TabularInline):
    model = MenuItem
    # Сколько пустых строк для новых пунктов выводить сразу
    extra = 1

# 2. Регистрируем основную модель меню
@admin.register(Menu)
class MenuAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['name', 'slug']
    # Добавляем пункты на страницу редактирования меню
    inlines = [MenuItemInline]

# Простая регистрация
admin.site.register(Service)

# Регистрация с ограничением (чтобы настройки сайта были в единственном экземпляре)
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    # Запрещаем добавлять новые, если уже есть одна запись (опционально, логика реализуется отдельно)
    pass