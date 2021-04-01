from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models.fields import CharField


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

    # password = CharField(max_length=200, blank=True, null=True)


class Categories(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)


class Genres(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name, self.slug


class Titles(models.Model):
    name = models.TextField(max_length=50)
    year = models.SmallIntegerField()
    description = models.TextField(max_length=200, null=True, blank=True)
    genre = models.ManyToManyField(
        Genres, related_name='titles', blank=True,
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL, related_name='titles',
        null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pk',)


class Reviews(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)


class Comments(models.Model):
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ('-pub_date',)
