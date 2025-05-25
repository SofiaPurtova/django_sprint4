from django import forms
from django.utils import timezone

from .models import Comment, Post


# Форма для создания/редактирования поста
class CreatePostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(
        initial=timezone.now,  # Устанавливаем текущую дату/время по умолчанию
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
            },
            format='%Y-%m-%dT%H:%M',  # Формат даты/времени
        ),
    )

    class Meta:
        model = Post
        fields = (
            'title',
            'image',
            'text',
            'pub_date',
            'location',
            'category',
            'is_published',
        )  # Поля, которые будут в форме


# Форма для создания комментария
class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)  # Только поле текста комментария
