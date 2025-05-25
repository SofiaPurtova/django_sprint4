from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CreateCommentForm, CreatePostForm
from .models import Category, Comment, Post, User
from .mixins import (CommentEditMixin, PostsEditMixin)
from .utils import (filter_published_posts)

# Количество постов на странице при пагинации
PAGINATED_BY = 10


class PostDeleteView(PostsEditMixin, LoginRequiredMixin, DeleteView):
    """Удаление поста с проверкой авторства."""
    model = Post
    success_url = reverse_lazy('blog:index')  # Перенаправление после удаления
    pk_url_kwarg = 'post_id'  # Имя параметра URL для ID поста

    def delete(self, request, *args, **kwargs):
        """Проверяет, является ли пользователь автором поста перед удалением."""
        post = get_object_or_404(Post, pk=self.kwargs[self.pk_url_kwarg])
        if self.request.user != post.author:
            return redirect('blog:index')
        return super().delete(request, *args, **kwargs)


class PostUpdateView(PostsEditMixin, LoginRequiredMixin, UpdateView):
    """Редактирование поста с проверкой авторства."""
    form_class = CreatePostForm  # Форма для редактирования
    model = Post
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        """Проверяет права на редактирование перед обработкой запроса."""
        post = get_object_or_404(Post, pk=self.kwargs[self.pk_url_kwarg])
        if self.request.user != post.author:
            return redirect('blog:post_detail', post_id=self.kwargs[self.pk_url_kwarg])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """URL для перенаправления после успешного редактирования."""
        return reverse('blog:post_detail', args=[self.kwargs[self.pk_url_kwarg]])


class PostCreateView(PostsEditMixin, LoginRequiredMixin, CreateView):
    """Создание нового поста."""
    model = Post
    form_class = CreatePostForm

    def form_valid(self, form):
        """Устанавливает автора поста перед сохранением."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """Перенаправляет в профиль автора после создания."""
        return reverse('blog:profile', args=[self.request.user.username])


class CommentCreateView(CommentEditMixin, LoginRequiredMixin, CreateView):
    """Создание комментария к посту."""
    model = Comment
    form_class = CreateCommentForm

    def form_valid(self, form):
        """Устанавливает пост и автора перед сохранением."""
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentDeleteView(CommentEditMixin, LoginRequiredMixin, DeleteView):
    """Удаление комментария с проверкой авторства."""
    model = Comment
    pk_url_kwarg = 'comment_id'  # Имя параметра URL для ID комментария

    def delete(self, request, *args, **kwargs):
        """Проверяет права на удаление перед выполнением."""
        comment = get_object_or_404(Comment, pk=self.kwargs[self.pk_url_kwarg])
        if self.request.user != comment.author:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().delete(request, *args, **kwargs)


class CommentUpdateView(CommentEditMixin, LoginRequiredMixin, UpdateView):
    """Редактирование комментария с проверкой авторства."""
    model = Comment
    form_class = CreateCommentForm
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        """Проверяет права на редактирование перед обработкой запроса."""
        comment = get_object_or_404(Comment, pk=self.kwargs[self.pk_url_kwarg])
        if self.request.user != comment.author:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class AuthorProfileListView(ListView):
    """Список постов конкретного автора."""
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = PAGINATED_BY  # Количество постов на странице

    def get_queryset(self):
        """Фильтрует посты автора (только опубликованные для чужих пользователей)."""
        author = get_object_or_404(User, username=self.kwargs['username'])
        posts = author.posts.all()
        if self.request.user != author:
            posts = filter_published_posts(posts)
        return posts

    def get_context_data(self, **kwargs):
        """Добавляет информацию об авторе в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(User, username=self.kwargs['username'])
        return context


class BlogIndexListView(ListView):
    """Главная страница со списком всех опубликованных постов."""
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'  # Имя переменной в шаблоне
    paginate_by = PAGINATED_BY

    queryset = filter_published_posts(Post.objects)  # Только опубликованные посты


class BlogCategoryListView(ListView):
    """Список постов определенной категории."""
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = PAGINATED_BY

    def get_queryset(self):
        """Фильтрует посты по категории (только опубликованные)."""
        category_slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=category_slug, is_published=True)
        return filter_published_posts(category.posts.all())


class PostDetailView(DetailView):
    """Детальная страница поста."""
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'  # Имя параметра URL для ID поста

    def get_context_data(self, **kwargs):
        """Добавляет форму комментария и список комментариев в контекст."""
        context = super().get_context_data(**kwargs)
        context['form'] = CreateCommentForm()  # Форма для добавления комментария
        context['comments'] = self.get_object().comments.prefetch_related('author').all()
        return context

    def get_object(self, queryset=None):
        """Возвращает пост, проверяя права на просмотр неопубликованных."""
        post = get_object_or_404(Post, pk=self.kwargs.get(self.pk_url_kwarg))
        if self.request.user == post.author:
            return post
        return get_object_or_404(
            filter_published_posts(Post.objects.all()),
            pk=self.kwargs.get(self.pk_url_kwarg)
        )
