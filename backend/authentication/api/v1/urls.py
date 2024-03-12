from django.urls import include
from django.urls import path
from django.conf import settings
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.renderers import BrowsableAPIRenderer
from core.renderers import BaseJSONRenderer
from authentication.views import UserViewSet, LoginView, LogoutView


TokenRefreshView.renderer_classes = [BaseJSONRenderer, BrowsableAPIRenderer]

router = routers.DefaultRouter(trailing_slash=settings.APPEND_SLASH)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
