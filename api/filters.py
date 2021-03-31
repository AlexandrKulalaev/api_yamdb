import django_filters

from .models import Titles


class ModelFilterTitles(django_filters.FilterSet):
    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='icontains'
    )
    category = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='icontains'
    )
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )

    class Meta:
        model = Titles
        fields = ['year']
