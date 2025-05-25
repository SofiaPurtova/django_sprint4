from typing import List
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, include, path

# Кастомные обработчики ошибок:
handler403 = 'pages.views.permission_denied'  # Ошибка 403 - Доступ запрещен
handler404 = 'pages.views.page_not_found'     # Ошибка 404 - Страница не найдена  
handler500 = 'pages.views.server_error'      # Ошибка 500 - Ошибка сервера

# Основные URL-шаблоны проекта:
urlpatterns: List[URLPattern] = [
    path('pages/', include('pages.urls', namespace='pages')),  # Страницы сайта
    path('', include('users.urls', namespace='users')),        # Пользовательские URL
    path('', include('blog.urls', namespace='blog')),          # Блог (главная страница)
    path('auth/', include('django.contrib.auth.urls')),       # Стандартные auth URL
    path('admin/', admin.site.urls),                         # Админ-панель
]

# Включение debug_toolbar только в режиме разработки
if settings.DEBUG:
    import debug_toolbar
    # Добавляем URL для отладки
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

# Обслуживание медиа-файлов в development режиме
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)