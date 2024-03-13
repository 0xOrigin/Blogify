from django.shortcuts import render
from core.views import BaseViewSet
from blog.models import Post
from blog.serializers import PostSerializer
from blog.filters import PostFilter
from blog.permissions import BlogPermissions


class PostViewSet(BaseViewSet):
    model = Post
    queryset = model.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter
    permission_classes = [BlogPermissions,]

    def get_queryset(self):
        return super().get_queryset().select_related('author')
