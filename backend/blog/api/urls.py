from django.urls import include
from django.urls import path


urlpatterns = [
    path('v1/', include('blog.api.v1.urls'), name='blog-api-v1'),
]
