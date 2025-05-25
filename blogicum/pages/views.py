from django.shortcuts import render
from django.views.generic import TemplateView


class AboutTemplateView(TemplateView):
    """Класс-представление для страницы 'О проекте'."""
    template_name = 'pages/about.html'  # Указывает используемый шаблон


class RulesTemplateView(TemplateView):
    """Класс-представление для страницы 'Правила'."""
    template_name = 'pages/rules.html'  # Указывает используемый шаблон


def permission_denied(request, exception):
    """
    Обработчик ошибки 403 (Доступ запрещен).
    Возвращает кастомную страницу с соответствующим HTTP-статусом.
    """
    return render(request, 'pages/403.html', status=403)


def csrf_failure(request, reason=''):
    """
    Обработчик ошибки CSRF (403 Forbidden при неверном CSRF-токене).
    Возвращает специализированную страницу ошибки.
    """
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    """
    Обработчик ошибки 404 (Страница не найдена).
    Принимает exception для возможного логирования, но не использует его в шаблоне.
    """
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """
    Обработчик ошибки 500 (Ошибка сервера).
    Используется при необработанных исключениях в коде.
    """
    return render(request, 'pages/500.html', status=500)
