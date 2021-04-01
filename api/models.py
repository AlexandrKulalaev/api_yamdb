from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
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


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('slug',)


class Genre(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('slug',)


class Title(models.Model):
    name = models.TextField(max_length=50)
    year = models.SmallIntegerField( validators=[year_validator])
    description = models.TextField(max_length=200, null=True, blank=True)
    genre = models.ManyToManyField(
        Genre, related_name='titles', blank=True,
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles',
        null=True, blank=True
    )

    class Meta:
        ordering = ('id',)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Оценка не может быть меньше 1'),
            MaxValueValidator(10, message='Оенка не может быть больше 10')
        ]
    )
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
