from django.db import models
from django.conf import settings
from core.models import BaseAuditModel


class Post(BaseAuditModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')

    def __str__(self) -> str:
        return f'{self.title} by {self.author}'
