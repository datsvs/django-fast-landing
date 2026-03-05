from django import template
# Предположим, у вас есть модель меню
from core.models import FeatureSection

register = template.Library()

@register.inclusion_tag('file-loader/loader.html', takes_context=True)
def show_feature(context, slug, template_name='feature-default'):
    try:
        # Получаем объект меню целиком вместе с элементами
        feature = FeatureSection.objects.prefetch_related('cards').get(slug=slug)
        cards = feature.cards.all().order_by('order')
    except FeatureSection.DoesNotExist:
        feature = None
        cards = []
    # Формируем путь к конкретному файлу верстки
    full_template_path = f'feature/{template_name}.html'
    return {
        'feature': feature,
        'feature_cards': cards,
        'template_name': full_template_path,
        # Чтобы работали активные ссылки
        'request': context.get('request'),
    }