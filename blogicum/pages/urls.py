from django.urls import path
from django.views.generic import TemplateView  # Импорт класса для статических страниц

# Пространство имен для URL-адресов приложения pages
app_name = 'pages'

# URL-шаблоны статических страниц
urlpatterns = [
    # Страница "О проекте"
    path(
        'about/', 
        TemplateView.as_view(template_name='pages/about.html'),
        name='about'
    ),

    # Страница "Правила"
    path(
        'rules/', 
        TemplateView.as_view(template_name="pages/rules.html"),
        name='rules'
    ),
]