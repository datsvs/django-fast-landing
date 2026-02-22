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