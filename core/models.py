# Для проведения санитаризации с помощью django-nh3
import nh3
from django.db import models
# Текстовое поле с поддержкой HTML и встроенным редактором CKEditor 5
from django_ckeditor_5.fields import CKEditor5Field
# Для доступа к настройкам из модели (например, для получения разрешенных тегов и атрибутов)
from django.conf import settings

# B админке объект Menu, внизу ты увидишь таблицу со всеми его MenuItems.
class Menu(models.Model):
    title = models.CharField("Название меню", max_length=100)
    slug = models.SlugField("Слаг", unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Меню сайта"
        verbose_name_plural = "Меню сайта"

# Создание пунктов меню в админке
class MenuItem(models.Model):
    # Добавляем связь ForeignKey
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    title = models.CharField("Название", max_length=100)
    url = models.CharField("Ссылка", max_length=200, help_text="Например: #about или https://google.com")
    order = models.PositiveIntegerField("Порядок", default=0)

    def __str__(self):
        return self.title
    # Сортируем по полю order, затем по title и id для стабильности порядка
    class Meta:
        ordering = ['order', 'title', 'id']
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

# B админке объект Tab, внизу ты увидишь таблицу со всеми его TabItem.
class Tab(models.Model):
    title = models.CharField("Название группы табов", max_length=100)
    slug = models.SlugField("Слаг", unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Группа табов"
        verbose_name_plural = "Группы табов"

# Создание табов в админке
class TabItem(models.Model):
    # Добавляем связь ForeignKey
    group = models.ForeignKey(Tab, related_name='tabs', on_delete=models.CASCADE)
    title = models.CharField("Заголовок таба", max_length=50)
    content = CKEditor5Field('Контент', config_name='default')
    order = models.PositiveIntegerField("Порядок", default=0)

    def __str__(self):
        return self.title
    # Сортируем по полю order, затем по title и id для стабильности порядка
    class Meta:
        ordering = ['order', 'title', 'id']
        verbose_name = "Таб"
        verbose_name_plural = "Табы"

    def save(self, *args, **kwargs):
        if self.content:
            # Используем .get() или getattr, чтобы иметь "запасной" пустой набор
            tags = getattr(settings, 'NH3_ALLOWED_TAGS', set())
            attrs = getattr(settings, 'NH3_ALLOWED_ATTRIBUTES', {})
            
            self.content = nh3.clean(
                self.content,
                tags=tags,
                attributes=attrs
            )
        super().save(*args, **kwargs)

# Модель для самой секции (группирует карточки)
class FeatureSection(models.Model):
    title = models.CharField("Название секции", max_length=200)
    slug = models.SlugField("Слаг", unique=True)

    def __str__(self):
            return self.title

    class Meta:
        verbose_name = "Секция преимуществ"
        verbose_name_plural = "Секции преимуществ"

# Модель отдельной карточки преимущества
class FeatureCard(models.Model):
    section = models.ForeignKey(FeatureSection, related_name="cards", on_delete=models.CASCADE, verbose_name="Секция")
    # Поле для иконки (можно вставлять название класса LineIcons)
    icon_code = models.CharField("Класс иконки", max_length=50, help_text="Введите класс иконки")
    title = models.CharField("Заголовок", max_length=100)
    # Описание с использованием CKEditor 5
    content = CKEditor5Field("Описание", config_name='default')
    order = models.PositiveIntegerField("Порядок", default=0)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order', 'title', 'id']
        verbose_name = "Карточка преимущества"
        verbose_name_plural = "Карточки преимуществ"

    def save(self, *args, **kwargs):
        if self.content:
            # Используем .get() или getattr, чтобы иметь "запасной" пустой набор
            tags = getattr(settings, 'NH3_ALLOWED_TAGS', set())
            attrs = getattr(settings, 'NH3_ALLOWED_ATTRIBUTES', {})
            
            self.content = nh3.clean(
                self.content,
                tags=tags,
                attributes=attrs
            )
        super().save(*args, **kwargs)

# Модель для общих настроек (Заголовок, лого, контакты)
class SiteSettings(models.Model):
    title = models.CharField("Заголовок сайта", max_length=200)
    logo = models.ImageField("Логотип", upload_to='images/')
    contact_email = models.EmailField("Email для связи")
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

# Модель для секции "Услуги" или "Преимущества"
class Service(models.Model):
    title = models.CharField("Название услуги", max_length=100)
    description = models.TextField("Описание")
    icon = models.ImageField("Иконка", upload_to='services/', blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"