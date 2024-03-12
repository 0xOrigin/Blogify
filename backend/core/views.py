from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.renderers import BrowsableAPIRenderer
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.paginations import BasePagination
from core.permissions import BasePermissions
from core.renderers import BaseJSONRenderer


# TODO: Implement rate limiting for all views (Must be concurrency safe)
class BaseViewSet(viewsets.ModelViewSet):
    model = None
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = BasePagination
    permission_classes = [BasePermissions,]
    renderer_classes = [BaseJSONRenderer, BrowsableAPIRenderer]

    def get_queryset(self):
        if self.model is None:
            raise NotImplementedError(_('BaseViewSet must be subclassed with a model'))
        return self.model.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, created_at=timezone.now())
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, updated_at=timezone.now())


class NonCreatableViewSet(viewsets.ModelViewSet):
    
    def create(self, request, *args, **kwargs):
        return Response({'detail': _('Method Not Allowed')}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class NonUpdatableViewSet(viewsets.ModelViewSet):

    def update(self, request, *args, **kwargs):
        return Response({'detail': _('Method Not Allowed')}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': _('Method Not Allowed')}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class NonDeletableViewSet(viewsets.ModelViewSet):

    def destroy(self, request, *args, **kwargs):
        return Response({'detail': _('Method Not Allowed')}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
