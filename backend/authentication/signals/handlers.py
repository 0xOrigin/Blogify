from django.dispatch import receiver
from django.db.models.signals import post_migrate, pre_save
from django.contrib.auth import get_user_model
from authentication.apps import AuthenticationConfig
from authentication.utils import create_superuser

User = get_user_model()

@receiver(post_migrate)
def perform_post_migrate_actions(sender, **kwargs):
    if sender.name == AuthenticationConfig.name:
        create_superuser() # Create superuser if not exists
