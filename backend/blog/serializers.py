from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.serializers import BaseSerializer
from blog.models import Post

User = get_user_model()


class AuthorSerializer(BaseSerializer):
    name = serializers.SerializerMethodField(source='get_name')

    class Meta:
        model = User
        exclude = BaseSerializer.Meta.exclude + (
            'groups', 'user_permissions', 'password', 'date_joined',
            'last_login', 'is_superuser', 'is_staff', 'is_active',
        )

    def get_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


class PostSerializer(BaseSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        exclude = ('created_by', 'updated_by',)
        extra_kwargs = {
            'author': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        instance = super().create(validated_data)
        return instance
