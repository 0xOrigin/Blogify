from rest_framework_nested import routers
from django.urls import include
from django.urls import path
from django.conf import settings
from blog.views import PostViewSet


router = routers.DefaultRouter(trailing_slash=settings.APPEND_SLASH)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
