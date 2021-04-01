from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CommentViewSet,
    ReviewViewSet,
    CategoriesViewSet,
    GenresViewSet,
    TitlesViewSet,
    UsersViewSet,
    emailConfirmation,
    SendToken,
)


router_v1 = DefaultRouter()
router_v1.register('users', UsersViewSet, basename='user_api')
router_v1.register('categories', CategoriesViewSet, basename='categories_api')
router_v1.register('genres', GenresViewSet, basename='genres_api')
router_v1.register('titles', TitlesViewSet, basename='titles_api')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    'review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    'comment'
)

urlpatterns = [
    path('auth/email/', emailConfirmation),
    path('auth/token/', SendToken),
    path('v1/', include(router_v1.urls)),
]
