from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class BaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = None
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by',)

    def create(self, validated_data):
        if self.Meta.model is None:
            raise NotImplementedError(_('BaseSerializer must be subclassed with a model'))
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if self.Meta.model is None:
            raise NotImplementedError(_('BaseSerializer must be subclassed with a model'))
        return super().update(instance, validated_data)
