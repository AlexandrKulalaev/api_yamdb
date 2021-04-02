from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import ModelFilterTitles
from .mixins import DestroyListCreateViewSet
from .models import Category, Genre, Review, Title
from .permissions import GeneralPermission, IsAdmin, IsAuthorModerAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          ConfirmationCodeSerializer, GenreSerializer,
                          ReviewSerializers, TitleReadSerializer,
                          TitleWriteSerializer, UserSerializer)

User = get_user_model()


@csrf_exempt
def email_confirmation(request):
    if request.method != 'POST':
        return JsonResponse(data={'Error': 'Request method not allowed', })

    email = request.POST.get('email')
    if email == '':
        return JsonResponse(data={'Error': 'Email not recieved', })

    user = get_object_or_404(User, email=email)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='email_confirmation',
        message=confirmation_code,
        from_email=settings.ADMIN_EMAIL,
        recipient_list=[email, ]
    )
    return JsonResponse(
        data='Confirmation code was sent to your email',
        safe=False
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def send_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data['confirmation_code']
    email = serializer.validated_data['email']

    user = get_object_or_404(User, email=email)
    token_check = default_token_generator.check_token(user, confirmation_code)

    if token_check is True:
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        refresh_token = str(refresh)
        access_token = str(access)
        return JsonResponse(
            data={'refresh': refresh_token, 'access': access_token}
        )
    return JsonResponse(
        data='Не верный Confirmation code',
        safe=False
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [IsAdmin, ]
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(DestroyListCreateViewSet):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = [GeneralPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class GenreViewSet(DestroyListCreateViewSet):
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = [GeneralPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filter_backends = [DjangoFilterBackend]
    filter_class = ModelFilterTitles
    permission_classes = [GeneralPermission]

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleWriteSerializer
        return TitleReadSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorModerAdmin]

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review_id=review.id)

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        queryset = review.comments.all()
        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorModerAdmin]

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        queryset = title.reviews.all()
        return queryset
