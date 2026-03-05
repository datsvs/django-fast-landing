from django.contrib import admin
# локальные файлы: Если вы хотите дать ссылку не на сайт, а на файл внутри вашего проекта
# (например, PDF-инструкцию в папке static), используйте функцию static
from django.templatetags.static import static
# Для отображения картинок в админке (например, для карточек фичей)
from django.utils.html import format_html
# Специальный миксин для инлайнов
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from .models import Menu, MenuItem, Tab, TabItem, FeatureSection, FeatureCard, SiteSettings, Service

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
    list_display = ('title', 'slug')
    # Автозаполнение slug из title
    prepopulated_fields = {'slug': ('title',)}
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

# 3.1 Описываем, как карточки будут выглядеть внутри секции
class FeatureCardInline(SortableInlineAdminMixin, admin.StackedInline):
    model = FeatureCard
    # Поля, которые будут отображаться при добавлении/редактировании карточек внутри группы
    fields = ('title', 'content', 'icon_code')
    # Если новая запись, то показываем 1 пустую строку, иначе - 0
    # (чтобы не было лишних пустых полей при редактировании существующих feature cards)
    def get_extra(self, request, obj=None, **kwargs):
        return 1 if obj is None else 0
    # Добавляем подсказку для поля icon_code, чтобы администраторы знали, как использовать иконки
    # В классах TabularInline и StackedInline метод get_form не работает,
    # так как он предназначен только для основного класса ModelAdmin.
    # Есть три способа добавить подсказку для полей в инлайне:
    # 1. Переопределить метод get_formset и добавить подсказку там (нагрузка средня).
    # 2. Использовать formfield_for_dbfield для конкретного поля (нагрузка легкая).
    # 3. ModelForm, если полей много, или если вам нужна сложная валидация в инлайне..
    # Переопределяем подсказку конкретно здесь
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Находим поле в базовой форме набора
        field = formset.form.base_fields.get('icon_code')
        if field:
            field.help_text = format_html(
                'Используйте иконки из <a href="{}" target="_blank">LineIcons 4.0 Library</a>',
                static('files/LineIcons 4.0 Viewer.html')
            )
        return formset

# 3.2 Регистрируем основную модель секции
@admin.register(FeatureSection)
class FeatureSectionAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('title', 'slug')
    # Автозаполнение slug из title
    prepopulated_fields = {"slug": ("title",)}
    inlines = [FeatureCardInline]

# Простая регистрация
admin.site.register(Service)

# Регистрация с ограничением (чтобы настройки сайта были в единственном экземпляре)
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    # Запрещаем добавлять новые, если уже есть одна запись (опционально, логика реализуется отдельно)
    pass