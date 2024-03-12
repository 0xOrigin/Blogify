import uuid
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class BaseQuerySet(models.QuerySet):
    pass


class BaseManager(models.Manager):

    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    objects = BaseManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True


class BaseAuditModel(BaseModel):
    created_at = models.DateTimeField(verbose_name=_('Created at'))
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Updated at'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_created_by', verbose_name=_('Created by'))
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_updated_by', verbose_name=_('Updated by'))

    class Meta:
        abstract = True
