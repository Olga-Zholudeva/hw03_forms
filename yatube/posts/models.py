from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг')
    description = models.TextField(
        verbose_name='Описание'
    )

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Содержание'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата написания'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Тематическая группа'
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.text[:100]
