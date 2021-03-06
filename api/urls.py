from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet,
                    email_confirmation, send_token)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='user_api')
router_v1.register('categories', CategoryViewSet, basename='categories_api')
router_v1.register('genres', GenreViewSet, basename='genres_api')
router_v1.register('titles', TitleViewSet, basename='titles_api')
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
    path('v1/auth/email/', email_confirmation),
    path('v1/auth/token/', send_token),
    path('v1/', include(router_v1.urls)),
]
