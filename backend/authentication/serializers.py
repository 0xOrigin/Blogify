from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login, Group
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.serializers import BaseSerializer
from core.utils import get_attr_in_lang

User = get_user_model()

class UserSerializer(BaseSerializer):
    name = serializers.SerializerMethodField(source='get_name')

    class Meta:
        model = User
        exclude = BaseSerializer.Meta.exclude + ('groups', 'user_permissions',)
        extra_kwargs = {
            'last_login': {'read_only': True},
            'password': {'write_only': True},
        }
    
    def validate_password(self, value):
        try:
            validate_password(value)
        except Exception as exception:
            raise serializers.ValidationError(exception.messages)
        return value

    def create(self, validated_data):
        validated_data['email'] = BaseUserManager.normalize_email(validated_data['email'])
        validated_data['password'] = make_password(validated_data['password'])

        with transaction.atomic():
            instance = super().create(validated_data)
            instance.groups.add(Group.objects.get(name=instance.role))
        
        return instance

    def get_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


class BaseTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'
    default_error_messages = {
        'no_active_account': _('Invalid username or password')
    }

    def validate(self, attrs):
        data = super().validate(attrs)

        data['access_token'] = data.pop('access')
        ROLE_SERIALIZERS = role_serializers_dict()
        if self.user.role in ROLE_SERIALIZERS:
            data[self.user.role] = ROLE_SERIALIZERS[self.user.role](self.user.role_object).data
        else:
            data['user'] = UserSerializer(self.user).data

        return data


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField(required=False)

    def extract_refresh_token(self):
        request = self.context['request']
        if 'refresh' in request.data and request.data['refresh'] != '':
            return request.data['refresh']
        
        cookie_name = settings.JWT_AUTH_REFRESH_COOKIE_NAME
        if cookie_name and cookie_name in request.COOKIES:
            return request.COOKIES.get(cookie_name)
        else:
            raise InvalidToken(_('No valid refresh token found'))

    def validate(self, attrs):
        attrs['refresh'] = self.extract_refresh_token()
        data = super().validate(attrs)
        data['access_token'] = data.pop('access')
        return data
