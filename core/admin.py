from django.contrib import admin
# Специальный миксин для инлайнов
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from .models import Menu, MenuItem, Tab, TabItem, SiteSettings, Service

# 1.1 Описываем, как пункты будут выглядеть внутри меню
class MenuItemInline(SortableInlineAdminMixin, admin.TabularInline):
    model = MenuItem
    # Поля, которые будут отображаться при добавлении/редактировании пунктов меню внутри группы
    fields = ('title', 'url')
    # Если новая запись, то показываем 1 пустую строку, иначе - 0
    # (чтобы не было лишних пустых полей при редактировании существующих пунктов меню)
    def get_extra(self, request, obj=None, **kwargs):
        return 1 if obj is None else 0

# 1.2 Регистрируем основную модель меню
@admin.register(Menu)
class MenuAdmin(SortableAdminBase, admin.ModelAdmin):
    ### В модели и тут исправить 'name' на 'title' (или наоборот, чтобы было единообразно)
    list_display = ('name', 'slug')
    # Автозаполнение slug из title
    prepopulated_fields = {'slug': ('name',)}
    inlines = [MenuItemInline]

# 2.1 Описываем, как табы будут выглядеть внутри меню
class TabItemInline(SortableInlineAdminMixin, admin.TabularInline):
    model = TabItem
    # Поля, которые будут отображаться при добавлении/редактировании табов внутри группы
    fields = ('title', 'content')
    # Если новая запись, то показываем 1 пустую строку, иначе - 0
    # (чтобы не было лишних пустых полей при редактировании существующих табов)
    def get_extra(self, request, obj=None, **kwargs):
        return 1 if obj is None else 0

# 2.2 Регистрируем основную модель таба
@admin.register(Tab)
class TabAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('title', 'slug')
    # Автозаполнение slug из title
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TabItemInline]

# Простая регистрация
admin.site.register(Service)

# Регистрация с ограничением (чтобы настройки сайта были в единственном экземпляре)
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    # Запрещаем добавлять новые, если уже есть одна запись (опционально, логика реализуется отдельно)
    pass