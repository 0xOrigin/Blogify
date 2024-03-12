from django_filters.rest_framework import filters, FilterSet
from django.db.models import Q
from blog.models import Post


class PostFilter(FilterSet):

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
            'content': ['icontains'],
        }
