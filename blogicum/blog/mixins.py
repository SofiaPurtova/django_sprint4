from django.urls import reverse
from .models import Comment, Post


# Миксин для редактирования постов (наследуется в PostCreateView/PostUpdateView)
class PostsEditMixin:
    model = Post  # Работаем с моделью Post
    template_name = 'blog/create.html'  # Используем этот шаблон


# Миксин для редактирования комментариев (наследуется в CommentCreateView/CommentUpdateView)
class CommentEditMixin:
    model = Comment  # Работаем с моделью Comment
    pk_url_kwarg = 'comment_pk'  # Имя параметра URL для ID комментария
    template_name = 'blog/comment.html'  # Используем этот шаблон

    def get_success_url(self):
        # После успешного сохранения перенаправляем на страницу поста
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])
