from django import template
# Предположим, у вас есть модель меню
from core.models import Tab

register = template.Library()

@register.inclusion_tag('file-loader/loader.html', takes_context=True)
def show_tabs(context, slug, template_name='tabs-default'):
    try:
        # Получаем объект меню целиком вместе с элементами
        tab = Tab.objects.prefetch_related('tabs').get(slug=slug)
        tabs = tab.tabs.all().order_by('order')
    except Tab.DoesNotExist:
        tab = None
        tabs = []
    # Формируем путь к конкретному файлу верстки
    full_template_path = f'tabs/{template_name}.html'
    return {
        'tab': tab,
        'tabs': tabs,
        'template_name': full_template_path,
        # Чтобы работали активные ссылки
        'request': context.get('request'),
    }