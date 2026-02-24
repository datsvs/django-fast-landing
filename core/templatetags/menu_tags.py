from django import template
# Предположим, у вас есть модель меню
from core.models import Menu

register = template.Library()

@register.inclusion_tag('menu/menu-loader.html', takes_context=True)
def show_menu(context, slug, template_name='menu-default'):
    try:
        # Получаем объект меню целиком вместе с элементами
        menu = Menu.objects.prefetch_related('items').get(slug=slug)
        items = menu.items.all().order_by('order')
    except Menu.DoesNotExist:
        menu = None
        items = []
    # Формируем путь к конкретному файлу верстки
    full_template_path = f'menu/{template_name}.html'
    return {
        'menu': menu,
        'menu_items': items,
        'template_name': full_template_path,
        # Чтобы работали активные ссылки
        'request': context.get('request'),
    }