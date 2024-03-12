from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from core.renderers import BaseJSONRenderer
from core.views import BaseViewSet, NonCreatableViewSet, NonUpdatableViewSet, NonDeletableViewSet
from authentication.jwt_auth import set_jwt_cookies, unset_jwt_cookies
from authentication.serializers import UserSerializer
from authentication.permissions import AuthenticationPermissions
from authentication.filters import UserFilter
from authentication.models import User


class UserViewSet(BaseViewSet):
    model = User
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AuthenticationPermissions]
    filterset_class = UserFilter

    def get_queryset(self):
        return (
            super().get_queryset().prefetch_related('groups', 'user_permissions')
        )


class LoginView(TokenObtainPairView):
    renderer_classes = [BaseJSONRenderer, BrowsableAPIRenderer]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        set_jwt_cookies(response, response.data['access_token'], response.data.pop('refresh'))
        return response


class LogoutView(generics.GenericAPIView):
    renderer_classes = [BaseJSONRenderer, BrowsableAPIRenderer]

    def get(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_200_OK)
        unset_jwt_cookies(response)
        return response
