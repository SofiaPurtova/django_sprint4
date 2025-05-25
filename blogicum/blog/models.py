from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Получаем модель пользователя
User = get_user_model()


class PublishedModel(models.Model):
    """Абстрактная модель с общими полями для публикаций."""
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        verbose_name="Добавлено", 
        auto_now_add=True,  # Устанавливается при создании
    )

    class Meta:
        abstract = True  # Абстрактная модель (не создает таблицу в БД)


class BaseTitle(models.Model):
    """Абстрактная модель для заголовков."""
    title = models.CharField(max_length=256, verbose_name='Заголовок')

    class Meta:
        abstract = True


class Location(PublishedModel):
    """Модель местоположения."""
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name


class Category(PublishedModel, BaseTitle):
    """Модель категории."""
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL',
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        """URL для страницы категории."""
        return reverse("blog:category_posts", kwargs={"category_slug": self.slug})


class Post(PublishedModel, BaseTitle):
    """Модель поста/публикации."""
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Можно делать отложенные публикации',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,  # Удалить пост при удалении автора
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.SET_NULL,  # Оставить пост при удалении локации
        null=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,  # Оставить пост при удалении категории
        null=True,
    )
    image = models.ImageField('Изображение', blank=True, upload_to='img/')

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)  # Сортировка по дате (новые сначала)
        default_related_name = 'posts'  # Имя для обратных связей

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        """URL для страницы поста."""
        return reverse("blog:post_detail", kwargs={"post_id": self.pk})


class Comment(models.Model):
    """Модель комментария."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments',  # Обратная связь для пользователя
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
        related_name='comments',  # Обратная связь для поста
    )
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(
        verbose_name='Дата',
        auto_now_add=True,  # Устанавливается при создании
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)  # Сортировка по дате (старые сначала)

    def __str__(self):
        return self.text[:20]  # Возвращаем первые 20 символов комментария
