from django.contrib import admin

from .models import Titles, Comments, Reviews, CustomUser


admin.site.register(CustomUser)


@admin.register(Titles)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title_id', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text', 'author')
    list_filter = ('author',)
    empty_value_display = '-пусто-'


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review_id', 'text', 'author', 'pub_date')
    search_fields = ('text', 'author',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'
