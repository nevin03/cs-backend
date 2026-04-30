import django_filters
from .models import FeaturedProject


class FeaturedProjectFilter(django_filters.FilterSet):
    tag = django_filters.CharFilter(lookup_expr="iexact", label="Filter by tag (case-insensitive)")
    tag_contains = django_filters.CharFilter(field_name="tag", lookup_expr="icontains")

    class Meta:
        model = FeaturedProject
        fields = ["tag"]
