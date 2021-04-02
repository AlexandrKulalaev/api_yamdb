from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator


class CustomUser(AbstractUser):
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='users biograpy'
    )
    email = models.EmailField(unique=True, verbose_name='email')
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOISE = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOISE,
        default='user',
        verbose_name='user role'
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Category(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='name_of_category'
    )
    slug = models.SlugField(unique=True, verbose_name='slug of category')

    class Meta:
        ordering = ('slug',)
        verbose_name = 'categoty'
        verbose_name_plural = 'categories'


class Genre(models.Model):
    name = models.CharField(max_length=30, verbose_name='name of genre')
    slug = models.SlugField(unique=True, verbose_name='slug of genre')

    class Meta:
        ordering = ('slug',)
        verbose_name = 'genre'
        verbose_name_plural = 'genres'


class Title(models.Model):
    name = models.TextField(max_length=50, verbose_name='name of title')
    year = models.SmallIntegerField(
        validators=[year_validator],
        verbose_name='year of title'
    )
    description = models.TextField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='description of title'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='genre'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'title'
        verbose_name_plural = 'titles'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='title',
    )
    text = models.TextField(verbose_name='text')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Оценка не может быть меньше 1'),
            MaxValueValidator(10, message='Оенка не может быть больше 10')
        ],
        verbose_name='score'
    )
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'review'
        verbose_name_plural = 'rewiews'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='review'
    )
    text = models.TextField(verbose_name='text of comment')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='author of comment')
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.text[:15]
