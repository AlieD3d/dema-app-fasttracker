from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import constraints

User = get_user_model()


class Place(models.Model):
    name = models.CharField(max_length=154)
    keywords = models.CharField(max_length=154)

    def __str__(self):
        return self.name[:15]


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Группы задач',
        help_text=''
    )
    description = models.TextField(
        max_length=255,
        verbose_name='Описание'
    )
    slug = models.SlugField(
        max_length=50,
        db_index=True,
        unique=True,
        verbose_name='URL'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Post(models.Model):
    text = models.TextField(
        max_length=200,
        verbose_name='Текст задачи',
        help_text='Введите текст задачи',
    )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относится задача'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-pub_date']


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        related_name='comments',
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        max_length=254,
        verbose_name='Комментарии'
    )
    created = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = (
            constraints.UniqueConstraint(
                fields=('user', 'author'), name='follow_unique'),
        )
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return self.user.username, self.author.username
