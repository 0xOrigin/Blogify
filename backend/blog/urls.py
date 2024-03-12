from django.urls import include
from django.urls import path
from blog.apps import BlogConfig

app_name = BlogConfig.name


urlpatterns = [
    path('api/', include('blog.api.urls'), name='blog-api'),
]
