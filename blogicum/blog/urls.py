from typing import List
from django.urls import URLPattern, path
from . import views

# Пространство имен для URL-адресов приложения
app_name = 'blog'

# Список URL-шаблонов приложения
urlpatterns: List[URLPattern] = [
    # Главная страница блога (список постов)
    path('', views.BlogIndexListView.as_view(), name='index'),

    # Страница детального просмотра поста
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),

    # Страница постов определенной категории
    path('category/<slug:category_slug>/', views.BlogCategoryListView.as_view(), name='category_posts'),

    # Страница профиля автора (список его постов)
    path('profile/<str:username>/', views.AuthorProfileListView.as_view(), name='profile'),

    # Создание нового поста
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),

    # Редактирование существующего поста
    path('posts/<int:post_id>/edit/', views.PostUpdateView.as_view(), name='edit_post'),

    # Удаление поста
    path('posts/<int:post_id>/delete/', views.PostDeleteView.as_view(), name='delete_post'),

    # Добавление комментария к посту
    path('posts/<int:post_id>/comment/', views.CommentCreateView.as_view(), name='add_comment'),

    # Редактирование комментария
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/', 
         views.CommentUpdateView.as_view(), name="edit_comment"),

    # Удаление комментария
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/', 
         views.CommentDeleteView.as_view(), name='delete_comment'),
]
