from django.db import models

# B админке объект Menu, внизу ты увидишь таблицу со всеми его MenuItems.
class Menu(models.Model):
    name = models.CharField("Название меню", max_length=100)
    slug = models.SlugField("Слаг", unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Меню сайта"
        verbose_name_plural = "Меню сайта"

# Создание меню в админке
class MenuItem(models.Model):
    # Добавляем связь ForeignKey
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    title = models.CharField("Название", max_length=100)
    url = models.CharField("Ссылка", max_length=200, help_text="Например: #about или https://google.com")
    order = models.PositiveIntegerField("Порядок", default=0)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order', 'title']

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