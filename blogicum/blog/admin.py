from django.contrib import admin
from .models import Category, Location, Post, Comment


# Админка для локаций
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')  # Отображаемые поля
    list_editable = ('is_published',)  # Редактируемые поля прямо в списке


# Админка для категорий
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'slug', 'is_published', 'created_at')
    list_editable = ('is_published',)


# Админка для постов
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'location', 'is_published', 'pub_date', 'comment_count')
    list_editable = ('is_published',)
    list_filter = ('category', 'location')  # Фильтры в правой панели

    # Метод для отображения количества комментариев
    @admin.display(description='Комментариев')
    def comment_count(self, post):
        return post.comments.count()


# Регистрация моделей с кастомными админ-классами
admin.site.register(Post, PostAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)  # Без кастомного админ-класса