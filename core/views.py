from django.shortcuts import render
from .models import SiteSettings, Service

def index(request):
    # Получаем первую запись настроек (или None, если пусто)
    settings = SiteSettings.objects.first()
    # Получаем все услуги
    services = Service.objects.all()
    
    context = {
        'settings': settings,
        'services': services,
    }
    return render(request, 'index.html', context)