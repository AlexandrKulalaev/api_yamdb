from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Comments, Reviews, Categories, Genres, Titles, CustomUser


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genres


class TitlesReadSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Titles
        fields = '__all__'
        read_only_fields = ('id', 'rating')


class TitlesWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        required=False,
        slug_field='slug',
        queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        required=False,
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Titles
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    review = serializers.ReadOnlyField(source='review.id')

    class Meta:
        fields = ('__all__')
        model = Comments


class ReviewsSerializers(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    score = serializers.FloatField(min_value=1, max_value=10)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Reviews

    def validate(self, data):
        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        method = self.context['request'].method

        if (Reviews.objects.filter(title=title_id, author=user)
                and method == 'POST'):
            raise serializers.ValidationError(
                'Нельзя написать 2 ревью для одного произведения'
            )
        return data


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'role',
            'email',
            'first_name',
            'last_name',
            'bio'
        )
